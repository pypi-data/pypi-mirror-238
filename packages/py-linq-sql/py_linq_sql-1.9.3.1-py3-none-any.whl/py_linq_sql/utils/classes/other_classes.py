"""Classes used in py-linq-sql."""

# Future imports
from __future__ import annotations

# Standard imports
from dataclasses import dataclass, field, fields
from typing import Any, TypeAlias

# Third party imports
from dotmap import DotMap
from psycopg import Connection

# Local imports
from .enum import CommandTypeOrStr, Terminal


def equality(obj: Any, other: Any) -> bool:  # noqa: ANN401
    """
    Try equality between two objects.

    obj_1 == obj_2.

    Args:
        - obj : first objects.
        - other : second objects.

    Returns:
        True if obj == other, False otherwise.
    """
    if not isinstance(other, type(obj)):
        return NotImplemented

    for self_attr, other_attr in zip(fields(obj), fields(other), strict=True):
        if not getattr(obj, self_attr.name) == getattr(other, other_attr.name):
            return False

    return True


# ---------------
# |  dataclass  |
# ---------------


@dataclass
class Command:
    """
    Class of command with command type and a string with a command of this type.

    Attributes:
        cmd_type (CommandType): Type of command.
        args (DotMap): All arguments for this command.
    """

    cmd_type: CommandTypeOrStr
    args: DotMap = field(default_factory=DotMap)

    def __eq__(self, other: Any) -> bool:  # noqa: ANN401
        """
        Try equality between two Command.

        Command_1 == Command_2.
        """
        if not isinstance(other, Command):
            return NotImplemented

        if not self.cmd_type == other.cmd_type:
            return False

        for key in self.args:
            if not self.args[key] == other.args[key]:
                return False

        return True

    def __ne__(self, other: Any) -> bool:  # noqa: ANN401
        """
        Try no-equality between two Command.

        Command_1 != Command_2.
        """
        return bool(not self.__eq__(other))


@dataclass
class Flags:
    """
    Class of flags for SQLEnumerable.

    Attributes:
        select (bool): True if we call `select()` method, False otherwise.
        alter (bool): True if we call an alter methods (insert, update),
            False otherwise.
        one (bool): True if we call a one methods (all, any, contains), False otherwise.
        terminal (Terminal): Type of terminal command.
        limit_offset (bool): True if we call a limit offset methods (see docs),
            False otherwise.
        join (bool): True if we call join methods (see docs), False otherwise.
        default_cmd (bool): True if we call default methods (see docs),
            False otherwise.

    """

    select: bool = False
    alter: bool = False
    one: bool = False
    terminal: Terminal | None = None
    limit_offset: bool = False
    join: bool = False
    default_cmd: bool = False

    def __eq__(self, other: Any) -> bool:  # noqa: ANN401
        """
        Try equality between two Flags.

        Flags_1 == Flags_2.
        """
        return equality(self, other)

    def __ne__(self, other: Any) -> bool:  # noqa: ANN401
        """
        Try no-equality between two Flags.

        Flags_1 != Flags_2.
        """
        return bool(not self.__eq__(other))

    def copy(self) -> Flags:
        """Create a shallow copy of self."""
        return Flags(
            self.select,
            self.alter,
            self.one,
            self.terminal,
            self.limit_offset,
            self.join,
            self.default_cmd,
        )


@dataclass
class SQLEnumerableData:
    """
    SQLEnumerable with only data for building.

    Attributes:
        connection (Connection) : Connection on which we want to execute the request.
        flags (Flags): All flags use to know the statement of the request.
        cmd (List[Command]): Commands we want to execute.
        table (str | SQLEnumerable): Table on which we want to execute the request.
        length (int | None): Length of the result of the request if we need else None.
    """

    connection: Connection
    flags: Flags
    cmd: list[Command]
    table: str | Any  # it's an SQLEnumerable
    length: int | None


# ---------------
# |  TypeAlias  |
# ---------------

PyLinqSqlInsertType: TypeAlias = (
    dict[str, Any] | list[dict[str, Any]] | tuple | list[tuple]
)
