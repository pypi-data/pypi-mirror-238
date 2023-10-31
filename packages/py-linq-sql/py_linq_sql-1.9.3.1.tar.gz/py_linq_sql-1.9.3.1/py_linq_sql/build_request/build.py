"""Build request for execution."""

# Standard imports
from typing import Set, cast

# Local imports
from ..exception.exception import UnknownCommandTypeError
from ..utils.classes.enum import CommandType as Ct
from ..utils.classes.other_classes import Command, SQLEnumerableData
from .alter import build_delete, build_insert, build_update
from .consult import build_group_join, build_join, build_select
from .one import build_all, build_any, build_contains


def _dispatch_one(command: Command, sqle: SQLEnumerableData) -> str:
    """
    Dispatch ONE command depending of his command type.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.

    Returns:
        Request to execute.

    Raises:
        psycopg.Error: Indirect raise by `build_all`, `build_any` or `build_contains`.
        TableError: Indirect raise by `build_all`, `build_any` or `build_contains`.
        TypeError: Indirect raise by `build_all`, `build_any` or `build_contains`.
        TypeOperatorError: Indirect raise by `build_all`, `build_any`
            or `build_contains`.
        ValueError: Indirect raise by `build_contains`.
    """
    match command.cmd_type:  # pylint: disable=duplicate-code
        case Ct.ANY:
            return build_any(command, sqle)
        case Ct.ALL:
            return build_all(command, sqle)
        case _:
            return build_contains(command, sqle)


def _dispatch_alter(
    command: Command,
    sqle: SQLEnumerableData,
    built_commands: Set[int],
) -> str:
    """
    Dispatch ALTER command depending of his command type.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        built_commands: All commands that have already been built.

    Returns:
        Request to execute.

    Raises:
        DeleteError: Indirect raise by `build_delete`.
        NeedWhereError: indirect raise by `build_delete`.
        psycopg.Error: Indirect raise by `build_delete` or `build_update`.
        TableError: Indirect raise by `build_delete` or `build_update`.
        TooManyReturnValueError: Indirect raise by `build_update`.
        TypeError: Indirect raise by `build_insert`, `build_delete` or `build_update`.
        TypeOperatorError: Indirect raise by `build_delete` or `build_update`.
        ValueError: Indirect raise by `build_insert`.
    """
    match command.cmd_type:
        case Ct.INSERT:
            return build_insert(command, sqle)
        case Ct.UPDATE:
            return build_update(command, sqle, built_commands)
        case _:
            return build_delete(command, sqle, built_commands)


def dispatch_build(
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
        Request to execute or None if command will run later.

    Raises:
        DeleteError: Indirect raise by `_dispatch_alter`.
        LengthMismatchError: Indirect raise by `build_join`.
        NeedWhereError: Indirect raise by `_dispatch_alter`.
        psycopg.Error: Indirect raise by
            `build_select`, `build_join`, `build_group_join`, `_dispatch_alter`
            or `_dispatch_one`.
        TableError: Indirect raise by
            `build_select`, `build_join`, `build_group_join`, `_dispatch_alter`
            or `_dispatch_one`.
        TooManyReturnValueError: Indirect raise by `_dispatch_alter`.
        TypeError: Indirect raise by
            `build_select`, `build_join`, `build_group_join`, `_dispatch_alter`,
            or `_dispatch_one`.
        TypeOperatorError: Indirect raise by
            `build_select`, `build_join`, `build_group_join`, `_dispatch_alter`,
            or`_dispatch_one`.
        UnknownCommandTypeError: If type of command not in Ct or
            indirect raise by `build_select`, `build_join` or `build_group_join`.
        ValueError: Indirect raise by `_dispatch_alter` or `_dispatch_one`.
    """
    result = None

    match command.cmd_type:
        case Ct.SELECT:
            result = build_select(command, sqle, built_commands)
        case Ct.JOIN:
            result = build_join(command, sqle, built_commands)
        case Ct.GROUP_JOIN:
            result = build_group_join(command, sqle, built_commands)
        case command.cmd_type if command.cmd_type in [Ct.INSERT, Ct.UPDATE, Ct.DELETE]:
            result = _dispatch_alter(command, sqle, built_commands)
        case command.cmd_type if command.cmd_type in [Ct.ANY, Ct.ALL, Ct.CONTAINS]:
            result = _dispatch_one(command, sqle)
        case command.cmd_type if command.cmd_type in list(Ct):  # type: ignore[operator]
            # HACK: The ignore above it's just the time that mypy supports the Strenum.
            # https://github.com/python/mypy/issues
            pass
        # The following case is just an other security layers,
        # but we can't go in this case for the moment.
        case _:  # pragma: no cover
            # HACK: The time that mypy supports the Strenum.
            # https://github.com/python/mypy/issues
            command_cmd_type = cast(Ct, command.cmd_type)
            raise UnknownCommandTypeError(command_cmd_type.value)

    return result


def build(sqle: SQLEnumerableData) -> str:
    """
    Build a list of commands from an SQLEnumerable.

    Args:
        sqle: SQLEnumerable contains list of commands to build.

    Returns:
        Request to execute.

    Raises:
        DeleteError: Indirect raise by `dispatch_build`.
        LengthMismatchError: Indirect raise by `dispatch_build`.
        NeedWhereError: Indirect raise by `dispatch_build`.
        psycopg.Error: Indirect raise by `dispatch_build`.
        TableError: Indirect raise by `dispatch_build`.
        TooManyReturnValueError: Indirect raise by `dispatch_build`.
        TypeError: Indirect raise by `dispatch_build`.
        TypeOperatorError: Indirect raise by `dispatch_build`.
        UnknownCommandTypeError: Indirect raise by `dispatch_build`.
        ValueError: Indirect raise by `dispatch_build`.
    """
    built_commands: Set[int] = set()
    commands = sqle.cmd
    if not commands:
        return ""

    result = []
    for idx, cmd in enumerate(commands):
        if idx not in built_commands:
            res = dispatch_build(cmd, sqle, built_commands)
            if res:
                result.append(res)
                built_commands.add(idx)

    # We use filter with None for the argument __function.
    # If we give None to the first element of filter
    # it will pass all the elements evaluate to false no matter why.
    #
    # We can have None in result if sqle.cmd contains commands
    # which will be evaluated later in build_select() or build_update()
    return " ".join(filter(None, result))
