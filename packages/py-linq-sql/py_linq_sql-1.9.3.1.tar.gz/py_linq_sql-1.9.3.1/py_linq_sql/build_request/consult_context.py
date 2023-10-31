"""Build all context consult commands."""

# Standard imports
from typing import Set, cast

# Local imports
from ..exception.exception import ReturnEmptyEnumerable
from ..utils.classes.enum import CommandType, CommandTypeOrStr
from ..utils.classes.other_classes import Command, SQLEnumerableData
from ..utils.functions.path_functions import get_paths
from ..utils.functions.predicate_functions import get_predicates_as_str

# --------------------
# |  Context builds  |
# --------------------


def build_order_by(
    command: Command,
    sqle: SQLEnumerableData,
    suffix: str = "ASC",
) -> str:
    """
    Build an order_by/order_by_descending request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        suffix: Suffix to add to define if we order by the begin or the end.
            By default: ASC (to begin).

    Returns:
        Sub request to execute.

    Raises:
        psycopg.Error: Indirect raise by `get_paths`.
        TableError: Indirect raise by `get_paths`.
        TypeError: Indirect raise by `get_paths`.
        TypeOperatorError: Indirect raise by `get_paths`.
    """
    fquery = command.args.fquery
    paths = get_paths(fquery, sqle)

    result = ["ORDER BY"]

    result.append(", ".join([f"{path} {suffix}" for path in paths]))

    return " ".join(result)


def define_one_begin_end(
    begin: int,
    end: int,
    number: int,
    type_: CommandTypeOrStr,
) -> tuple[int, int]:
    """
    Define the begin, end depending on the type of command and the old begin, end.

    Args:
        begin: The old begin, the first time its 0.
        end: The old end, the first time its the length of the table
            with all conditions.
        number: The number use to calculate the new begin or end.
        type_: Type of the command who was called.

    Returns:
        The new begin and the new end.

    Examples:
        With take:
        >>> define_one_begin_end(0, 7, 3, CommandType.TAKE)
        (0, 3)

        With skip:
        >>> define_one_begin_end(0, 7, 3, CommandType.SKIP)
        (3, 7)

        With take_last:
        >>> define_one_begin_end(0, 7, 3, CommandType.TAKE_LAST)
        (4, 7)

        With skip_last:
        >>> define_one_begin_end(0, 7, 3, CommandType.SKIP_LAST)
        (0, 4)
    """
    match type_:
        case CommandType.TAKE:
            end = min(begin + number, end)
        case CommandType.SKIP:
            begin = begin + number
        case CommandType.TAKE_LAST:
            new_begin = end - number
            if new_begin >= begin:
                begin = new_begin
        case CommandType.SKIP_LAST:
            end = end - number

    if end - begin <= 0:
        raise ReturnEmptyEnumerable
    return begin, end


def define_limit_offset(sqle: SQLEnumerableData, built_commands: Set[int]) -> str:
    """
    Define the final limit offset for an SQL command.

    Args:
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        built_commands: All commands that have already been built.

    Returns:
        The final limit offset with the correct syntax.

    Raises:
        TypeError: If sqle.length is None.
    """
    commands = sqle.cmd

    begin, end = 0, sqle.length

    # We ignore type on end because if we enter in this function,
    # we are sure that the size has been calculated beforehand.

    for idx, cmd in enumerate(commands):
        match cmd.cmd_type:
            case CommandType.TAKE:
                begin, end = define_one_begin_end(
                    begin,
                    cast(int, end),
                    cmd.args.number,
                    CommandType.TAKE,
                )
                built_commands.add(idx)
            case CommandType.SKIP:
                begin, end = define_one_begin_end(
                    begin,
                    cast(int, end),
                    cmd.args.number,
                    CommandType.SKIP,
                )
                built_commands.add(idx)
            case CommandType.TAKE_LAST:
                begin, end = define_one_begin_end(
                    begin,
                    cast(int, end),
                    cmd.args.number,
                    CommandType.TAKE_LAST,
                )
                built_commands.add(idx)
            case CommandType.SKIP_LAST:
                begin, end = define_one_begin_end(
                    begin,
                    cast(int, end),
                    cmd.args.number,
                    CommandType.SKIP_LAST,
                )
                built_commands.add(idx)
            case _:
                pass

    limit = cast(int, end) - begin
    offset = begin
    return f"LIMIT {limit} OFFSET {offset}"


def _build_one_where(
    command: Command,
    sqle: SQLEnumerableData,
    first: bool = True,
) -> str:
    """
    Build a where request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.

    Returns:
        Sub request to execute.

    Raises:
        psycopg.Error: Indirect raise by `get_predicates_as_str`.
        TableError: Indirect raise by `get_predicates_as_str`.
        TypeError: Indirect raise by `get_predicates_as_str`.
        TypeOperatorError: Indirect raise by `get_predicates_as_str`.
    """
    fquery = command.args.fquery

    result = ["WHERE"] if first else ["AND"]

    get_predicates_as_str(result, fquery, sqle)

    return " ".join(result)


def build_where(sqle: SQLEnumerableData, built_commands: Set[int]) -> str:
    """
    Build all where request.

    Args:
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        built_commands: All commands that have already been built.

    Returns:
        Sub request to execute.

    Raises:
        psycopg.Error: Indirect raise by `_build_one_where`.
        TableError: Indirect raise by `_build_one_where`.
        TypeError: Indirect raise by `_build_one_where`.
        TypeOperatorError: Indirect raise by `_build_one_where`.
    """
    commands = sqle.cmd
    first_where = False
    result = []

    for idx, cmd in enumerate(commands):
        if cmd.cmd_type == CommandType.WHERE:
            if not first_where:
                result.append(_build_one_where(cmd, sqle))
                first_where = True
                built_commands.add(idx)
            else:
                result.append(_build_one_where(cmd, sqle, first=False))
                built_commands.add(idx)

    return " ".join(result)
