"""Build all consult commands."""

# Standard imports
from typing import List, Set, Tuple, cast

# Third party imports
from dotmap import DotMap

# Local imports
from ..exception.exception import LengthMismatchError, UnknownCommandTypeError
from ..utils.classes.enum import CommandType, JoinType, Terminal
from ..utils.classes.magicdotpath import (
    BaseMagicDotPath,
    MagicDotPath,
    MagicDotPathAggregate,
)
from ..utils.classes.other_classes import Command, SQLEnumerableData
from ..utils.functions.aggregate_functions import get_aggregate
from ..utils.functions.join_functions import join_get_intersect, join_get_paths
from ..utils.functions.other_functions import _col_name_validator, get_columns_name
from ..utils.functions.path_functions import get_path
from ..utils.functions.predicate_functions import get_one_predicate_as_str
from .consult_context import build_order_by, build_where, define_limit_offset
from .consult_terminal import (
    build_count,
    build_distinct,
    build_except,
    build_group_by,
    build_intersect,
    build_max,
    build_min,
    build_union,
)

# All command type which must be processed at the beginning of the select.
_SELECT_ADD_CMD = [
    CommandType.MAX,
    CommandType.MIN,
    CommandType.COUNT,
    CommandType.DISTINCT,
]


def _dispatch_terminal(command: Command, sqle: SQLEnumerableData) -> str:
    """
    Dispatch command depending of his command type.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.

    Returns:
        Sub request to execute.

    Raises:
        UnknownCommandTypeError: If command.cmd_type not in CommandType.
        TypeError: Indirect raise by `build_max` or `build_min`.
        psycopg.Error: Indirect raise by `build_max` or `build_min`.
        TableError: Indirect raise by `build_max` or `build_min`.
        TypeOperatorError: Indirect raise by `build_max` or `build_min`.
    """
    match command.cmd_type:
        case CommandType.MAX:
            return build_max(command, sqle)
        case CommandType.MIN:
            return build_min(command, sqle)
        case CommandType.COUNT:
            return build_count()
        case CommandType.DISTINCT:
            return build_distinct()
        # The following case is just an other security layers,
        # but we can't go in this case for the moment.
        case _:  # pragma: no cover
            # HACK: The time that mypy supports the Strenum.
            # https://github.com/python/mypy/issues
            command_cmd_type = cast(CommandType, command.cmd_type)
            raise UnknownCommandTypeError(command_cmd_type.value)


def _dispatch_select(
    command: Command,
    sqle: SQLEnumerableData,
    built_commands: Set[int],
) -> str | None:
    """
    Dispatch command depending of his command type.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        built_commands: All commands that have already been built.

    Returns:
        Sub request to execute.

    Raises:
        UnknownCommandTypeError: If command.cmd_type not in CommandType.
        TypeError: Indirect raise by `build_where` or `build_order_by`.
        psycopg.Error: Indirect raise by `build_where` or `build_order_by`.
        TableError: Indirect raise by `build_where` or `build_order_by`.
        TypeOperatorError: Indirect raise by `build_where` or `build_order_by`.
    """
    result = None

    match command.cmd_type:  # pylint: disable=duplicate-code
        case CommandType.EXCEPT_:
            result = build_except(command)
        case CommandType.WHERE:
            result = build_where(sqle, built_commands)
        case CommandType.ORDER_BY:
            result = build_order_by(command, sqle)
        case CommandType.ORDER_BY_DESC:
            result = build_order_by(command, sqle, "DESC")
        case CommandType.UNION:
            result = build_union(command)
        case CommandType.INTERSECT:
            result = build_intersect(command)
        case command.cmd_type if (
            command.cmd_type in _SELECT_ADD_CMD or command.cmd_type in list(CommandType)
        ):
            pass
        # The following case is just an other security layers,
        # but we can't go in this case for the moment.
        case _:  # pragma: no cover
            raise UnknownCommandTypeError(
                command.cmd_type.value,  # type: ignore[attr-defined]
            )

    return result


def _build_select_addon(
    sqle: SQLEnumerableData,
    built_commands: Set[int],
) -> str:
    """
    Build all select addon commands.

    The select addons are the commands that are processed before the end of the select
    and which will come to the level of the selected element.
    Example: Max is a select addon because the selected member of the request is
    MAX(<jsonb_paths>)
    and the request is SELECT MAX(<jsonb_paths> FROM <table>.

    Args:
        sqle: SQLEnumerable which contains the list of commands.
        built_commands: All commands that have already been built.

    Returns:
        Sub request to execute with the select addon command found.

    Raises:
        TypeError: Indirect raise by `_dispatch_terminal`.
        psycopg.Error: Indirect raise by `_dispatch_terminal`.
        TableError: Indirect raise by `_dispatch_terminal`.
        TypeOperatorError: Indirect raise by `_dispatch_terminal`.
        UnknownCommandTypeError: Indirect raise by `_dispatch_terminal`.
    """
    cmd = None

    for idx, cmd in enumerate(sqle.cmd):
        if cmd.cmd_type in _SELECT_ADD_CMD:
            built_commands.add(idx)
            break

    return _dispatch_terminal(cmd, sqle)


def _build_context_and_terminal(
    result: List[str],
    sqle: SQLEnumerableData,
    built_commands: Set[int],
) -> None:
    """
    Build all commands who have not yet been build.

    Args:
        result: List of different parts of the request.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        built_command: All commands that have already been built.

    Raises:
        TypeError: Indirect raise by `_dispatch_select`.
        psycopg.Error: Indirect raise by `_dispatch_select`.
        TableError: Indirect raise by `_dispatch_select`.
        TypeOperatorError: Indirect raise by `_dispatch_select`.
        UnknownCommandTypeError: Indirect raise by `_dispatch_select`.
    """
    for idx, cmd in enumerate(sqle.cmd):
        if idx not in built_commands:
            if res := _dispatch_select(cmd, sqle, built_commands):
                result.append(res)
            built_commands.add(idx)

    if sqle.flags.limit_offset:
        result.append(define_limit_offset(sqle, built_commands))


def _build_join_clauses(result: List[str], paths: DotMap, join_type: JoinType) -> None:
    """
    Build the clauses of a join.

    Args:
        result: List of different parts of the request.
        paths: Different paths for the clauses, selected, outer and inner paths.
        join_type: Type of the join.
    """
    result.append(
        " AND ".join(
            [
                f"({path_outer_k})::text = ({path_inner_k})::text"
                for (path_outer_k, path_inner_k) in zip(
                    paths.outer_key_paths,
                    paths.inner_key_paths,
                )
            ],
        ),
    )

    if intersect := join_get_intersect(
        join_type,
        paths.outer_key_paths,
        paths.inner_key_paths,
    ):
        result.append(intersect)


# ----------------------
# |  Group Join build  |
# ----------------------


def _get_selected_by(
    mdps: MagicDotPath | Tuple[MagicDotPath | MagicDotPathAggregate],
) -> Tuple[str, str]:
    """
    Get the paths of select and group_by from MagicDotPaths.

    Args:
        mdps: MagicDotPath(s) from which we want to generate the paths.

    Returns:
        Sub request to execute.

    Raises:
        TypeError: If magic_dp is not a MagicDotPath
            or indirect raise by `get_aggregate` or `get_path`.
        psycopg.Error: Indirect raise by `get_one_aggregate` or `get_path`.
        TableError: Indirect raise by `get_one_aggregate` or `get_path`.
        TypeOperatorError: Indirect raise by `get_columns_name`.
    """
    selected = []
    by = []  # pylint: disable=invalid-name
    mdp_for_names = []
    match mdps:
        case MagicDotPath():
            by.append(get_path(mdps)[0])
            mdp_for_names.append(mdps)
        case tuple():
            for magic_dp in mdps:
                match magic_dp:
                    case MagicDotPath():
                        by.append(get_path(magic_dp)[0])
                        mdp_for_names.append(magic_dp)
                    case MagicDotPathAggregate():
                        selected.append(get_aggregate(magic_dp))
                    case _:
                        raise TypeError(
                            "_get_selected_by take only MagicDotPath, "
                            "tuple of MagicDotPath or tuple of MagicDotPathAggregate.",
                        )
        case dict():
            mdp_for_names = {}
            for key, value in mdps.items():
                match value:
                    case MagicDotPath():
                        by.append(get_path(value)[0])
                        mdp_for_names[key] = value
                    case MagicDotPathAggregate():
                        selected.append(
                            f"{get_aggregate(value)} AS {_col_name_validator(key)}"
                        )
                    case _:
                        raise TypeError(
                            "_get_selected_by take only MagicDotPath, "
                            "tuple of MagicDotPath or tuple of MagicDotPathAggregate.",
                        )
        case _:
            raise TypeError(
                "_get_selected_by take only MagicDotPath, "
                "tuple of MagicDotPath or tuple of MagicDotPathAggregate.",
            )

    names = get_columns_name(mdp_for_names)
    selected.insert(
        0,
        ", ".join([f"{path} AS {name}" for path, name in zip(by, names)]),
    )

    return ", ".join(selected), ", ".join(by)


def build_group_join(  # pylint: disable=too-many-locals
    command: Command,
    sqle: SQLEnumerableData,
    built_commands: Set[int],
) -> str:
    """
    Build a group join request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        built_commands: All commands that have already been built.

    Returns:
        Sub request to execute.

    Raises:
        psycopg.Error: Indirect raise by
            `_get_selected_by`, `get_path` or `_build_context_and_terminal`.
        TableError: Indirect raise by
            `_get_selected_by`, `get_path` or`_build_context_and_terminal`.
        TypeError: Indirect raise by
            `_get_selected_by`, `get_path` or `_build_context_and_terminal`.
        TypeOperatorError: Indirect raise by
            `_get_selected_by`, _build_context_and_terminal`,
            `BaseMagicDotPath._get_number_operator`
            or `BaseMagicDotPath._get_generic_operator`.
        UnknownCommandTypeError: Indirect raise by `_build_context_and_terminal`.
    """
    result_function = command.args.result_function
    outer = command.args.outer
    inner = command.args.inner
    outer_key = command.args.outer_key
    inner_key = command.args.inner_key
    join_type = command.args.join_type

    obj_inner = MagicDotPath(inner.connection, with_table=inner.table)
    obj_outer = MagicDotPath(outer.connection, with_table=outer.table)

    mdps = result_function(obj_inner, obj_outer)
    selected, by = _get_selected_by(mdps)  # pylint: disable=invalid-name

    result = [f"SELECT {selected}"]

    result.append(f"FROM {outer.table} {join_type.as_str} JOIN {inner.table} ON")

    paths = DotMap(
        outer_key_paths=get_path(outer_key(obj_outer)),
        inner_key_paths=get_path(inner_key(obj_inner)),
    )

    _build_join_clauses(result, paths, join_type)
    _build_context_and_terminal(result, sqle, built_commands)

    result.append(f"GROUP BY {by}")

    return " ".join(result)


# ----------------
# |  Join build  |
# ----------------


def build_join(  # pylint: disable=too-many-locals
    command: Command,
    sqle: SQLEnumerableData,
    built_commands: Set[int],
) -> str:
    """
    Build a join request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        built_commands: All commands that have already been built.

    Returns:
        Sub request to execute.

    Raises:
        LengthMismatchError: If len of path the outer_key is not equal to
            len of path of the inner key.
        psycopg.Error: Indirect raise by
            `join_get_paths`, `get_path` or `_build_context_and_terminal`.
        TableError: Indirect raise by
            `join_get_paths`, `get_path` or `_build_context_and_terminal`.
        TypeOperatorError: Indirect raise by
            `BaseMagicDotPath._get_number_operator`,
            `BaseMagicDotPath._get_generic_operator`, `get_columns_name`
            or `_build_context_and_terminal`.
        TypeError: Indirect raise by
            `join_get_paths`, `get_path` or `_build_context_and_terminal`.
        UnknownCommandTypeError: Indirect raise by `_build_context_and_terminal`.
    """
    outer = command.args.outer
    inner = command.args.inner
    outer_key = command.args.outer_key
    inner_key = command.args.inner_key
    result_function = command.args.result_function
    join_type = command.args.join_type

    paths = join_get_paths(outer, inner, inner_key, outer_key, result_function)

    if not len(paths.outer_key_paths) == len(paths.inner_key_paths):
        raise LengthMismatchError("outer_key_path", "inner_key_paths")

    result = ["SELECT"]

    if not paths.select_paths:
        result.append(f"{outer.table}.*, {inner.table}.*")
    else:
        obj_inner = MagicDotPath(inner.connection, with_table=inner.table)
        obj_outer = MagicDotPath(outer.connection, with_table=outer.table)
        mdp_select_paths = result_function(obj_inner, obj_outer)
        names = get_columns_name(mdp_select_paths)
        result.append(
            ", ".join(
                [f"{path} AS {name}" for path, name in zip(paths.select_paths, names)],
            ),
        )

    result.append(f"FROM {outer.table} {join_type.as_str} JOIN {inner.table} ON")

    _build_join_clauses(result, paths, join_type)
    _build_context_and_terminal(result, sqle, built_commands)

    return " ".join(filter(None, result))


# ------------------
# |  Select build  |
# ------------------


def build_select(
    command: Command,
    sqle: SQLEnumerableData,
    built_commands: Set[int],
) -> str:
    """
    Build a select request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        built_commands: All commands that have already been built.

    Returns:
        Request to execute.

    Raises:
        TypeError: If all commands are not subclasses of BaseMagicDotPath
            or Indirect raise by `_build_select_addon`, `get_one_predicate_as_str`,
            `_build_context_and_terminal` or `build_group_by`.
        psycopg.Error: Indirect raise by `_build_select_addon`,
            `get_one_predicate_as_str`, `_build_context_and_terminal`,
            or `build_group_by`.
        TableError: Indirect raise by `_build_select_addon`,
            `get_one_predicate_as_str`, `_build_context_and_terminal`,
            or `build_group_by`.
        TypeOperatorError: Indirect raise by `_build_select_addon`,
            `BaseMagicDotPath._get_number_operator`,
            `BaseMagicDotPath._get_generic_operator`, `get_columns_name`,
            `_build_context_and_terminal` or `build_group_by`.
        UnknownCommandTypeError: Indirect raise by `_build_select_addon`
            or`_build_context_and_terminal`.
    """
    fquery = command.args.fquery  # pylint: disable=duplicate-code

    result = ["SELECT"]

    term = (
        _build_select_addon(sqle, built_commands)
        if sqle.flags.terminal
        in [Terminal.MAX, Terminal.MIN, Terminal.COUNT, Terminal.DISTINCT]
        else None
    )

    if term:
        result.append(term)

    if not term or sqle.flags.terminal in [Terminal.DISTINCT]:
        if not fquery:
            result.append("*")
        else:
            mdp_w_path = fquery(MagicDotPath(sqle.connection))
            match mdp_w_path:
                case BaseMagicDotPath():
                    paths = [get_one_predicate_as_str(sqle, mdp_w_path)]
                case tuple():
                    paths = [get_one_predicate_as_str(sqle, mdp) for mdp in mdp_w_path]
                case dict():
                    paths = [
                        get_one_predicate_as_str(sqle, mdp)
                        for mdp in mdp_w_path.values()
                    ]
                case _:
                    raise TypeError(
                        "You must put a MagicDotPath in lambda, see the documentation.",
                    )
            names = get_columns_name(mdp_w_path)
            result.append(
                ", ".join([f"{path} AS {name}" for path, name in zip(paths, names)]),
            )

    # If we have a Group_by we build this
    # (the last command because it's a terminal command)
    # we append all aggregate built by `build_group_by()`
    # and we add to the built_commands the index of this group_by.
    if sqle.flags.terminal == Terminal.GROUP_BY:
        aggregates = build_group_by(sqle.cmd[-1], sqle)
        result.append(f", {aggregates}")
        built_commands.add(len(sqle.cmd) - 1)

    if isinstance(sqle.table, str):
        result.append(f"FROM {sqle.table}")
    else:
        result.append(f"FROM ({sqle.table.get_command()}) AS subrequest")

    _build_context_and_terminal(result, sqle, built_commands)

    if sqle.flags.terminal == Terminal.GROUP_BY:
        result.append("GROUP BY")
        result.append(", ".join(list(path for path in paths)))

    return " ".join(filter(None, result))
