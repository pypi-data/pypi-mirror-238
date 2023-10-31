"""SQLEnumerable objects and all methods of this class generate a SQL jsonb request."""
# pylint: disable=too-many-public-methods, too-many-lines,
# We disable pylint warning R0904 and C0302 because
# we implemented an api that specifically has a lot of public methods.

# Future imports
from __future__ import annotations

# Standard imports
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, cast

# Third party imports
from dotmap import DotMap
from psycopg import Connection, ProgrammingError
from py_linq import Enumerable

# Local imports
from ..build_request.build import build
from ..config.config import is_read_only, is_valid_table_name_with_white_and_black_list
from ..exception.exception import (
    ActionError,
    AlreadyExecutedError,
    AlterError,
    DeleteError,
    EmptyInputError,
    EmptyQueryError,
    GroupByWithJoinError,
    LengthMismatchError,
    MoreThanZeroError,
    NeedSelectError,
    NegativeNumberError,
    NoMaxOrMinAfterLimitOffsetError,
    OneError,
    OtherThanWhereError,
    ReadOnlyPermissionDeniedError,
    ReturnEmptyEnumerable,
    SelectError,
    TablePermissionDeniedError,
    TerminalError,
    UnknownCommandTypeError,
)
from ..utils.classes.enum import CommandType as Ct
from ..utils.classes.enum import CommandTypeOrStr as Ctos
from ..utils.classes.enum import JoinType, Terminal
from ..utils.classes.magicdotpath import (
    LambdaMagicDotPath,
    LambdaMagicDotPathAggregate,
    MagicDotPath,
)
from ..utils.classes.other_classes import (
    Command,
    Flags,
    PyLinqSqlInsertType,
    SQLEnumerableData,
    equality,
)
from ..utils.db import get_cursor
from ..utils.execute import execute_alter, execute_one, execute_select
from ..utils.functions.other_functions import safe
from ..utils.functions.path_functions import get_path


@dataclass
class SQLEnumerable:
    """
    SQLEnumerable objects with some specific methods.

    Attributes:
        connection (Connection): Connection on which we want to execute the request.
        table (str | SQLEnumerable): Table or an other request on which
            we want to execute the request.
        cmd (List[Command]): Commands we want to execute.
        flags (Flags): All flags use to know the statement of the request.
        executed (bool): Executed status, True if is already executed False otherwise.
        length (int | None): Length of the result of the request if we need else None.

    """

    connection: Connection
    table: str | SQLEnumerable
    cmd: List[Command] = field(default_factory=list, init=False)
    flags: Flags = field(default_factory=Flags)
    executed: bool = False
    length: int | None = None

    def __post_init__(self) -> None:
        """
        Initialize the command list and safe the table if it's an str.

        Raises:
            psycopg.Error: Indirect raise by `safe`.
            TablePermissionDeniedError: Indirect raise by
                `is_valid_table_name_with_white_and_black_list`.
        """
        if isinstance(self.table, str):
            tables = self.table.split(".") if "." in self.table else [self.table]
            safed_tables = []
            for table in tables:
                if not is_valid_table_name_with_white_and_black_list(table):
                    raise TablePermissionDeniedError(table)
                safed_tables.append(safe(self.connection, table))
            self.table = ".".join([f'"{stab[1:-1]}"' for stab in safed_tables])

        self.cmd = []

    def __eq__(self, other: Any) -> bool:
        """
        Try equality between two SQL_Enumerable.

        SQL_Enumerable_1 == SQL_Enumerable_2.
        """
        return equality(self, other)

    def __ne__(self, other: Any) -> bool:
        """
        Try no-equality between two SQL_Enumerable.

        SQL_Enumerable_1 != SQL_Enumerable_2.
        """
        return bool(not self.__eq__(other))

    def copy(self) -> SQLEnumerable:
        """Create a shallow copy of self."""
        return SQLEnumerable(
            self.connection,
            self._format_table(),
            self.flags.copy(),
            self.executed,
            self.length,
        )

    def _format_table(self) -> str | SQLEnumerable:
        if isinstance(self.table, str):
            return self.table[1:-1]
        return self.table

    def _only_where_command(self) -> bool:
        """Check if all methods call before are where commands."""
        for command in self.cmd:
            if not command.cmd_type == Ct.WHERE:
                return False

        return True

    def _check_select(
        self,
        sqle: SQLEnumerable,
        caller_name: str,
    ) -> None:
        """
        Check if all select are correct.

        Check if we we have select in self and sqle.
        Check if the length of those select are equals.

        To understand the 2 first expressions you can read:
        https://stackoverflow.com/questions/9542738/python-find-in-list/9542768#9542768
        With those expressions we get the first element who validate
        `command.cmd_type == Ct.SELECT` if no element validates we get None.

        Args:
            sqle: The second sqle to check (the first is self).
            caller_name: Name of the function call _check_select

        Raises:
            NeedSelectError: If there is no select in  self, or sqle (or both).
            LengthMismatchError: If the number of column selected are not equal.
            TypeError: Indirect raise by `get_path`.
            psycopg.Error: Indirect raise by `get_path`.
            TableError: Indirect raise by `get_path`.
        """
        self_select = next(
            (command for command in self.cmd if command.cmd_type == Ct.SELECT),
            None,
        )

        sqle_select = next(
            (command for command in sqle.cmd if command.cmd_type == Ct.SELECT),
            None,
        )

        match (self_select, sqle_select):
            case (None, _) | (_, None) | (None, None):
                raise NeedSelectError(caller_name)

        # From now on we recover fquerys and MagicDotPath to do test on it.

        self_fquery = self_select.args.fquery  # type: ignore[union-attr]
        sqle_fquery = sqle_select.args.fquery  # type: ignore[union-attr]

        mdp_self = self_fquery(MagicDotPath(self.connection)) if self_fquery else "all"
        mdp_sqle = sqle_fquery(MagicDotPath(sqle.connection)) if sqle_fquery else "all"

        match (mdp_self, mdp_sqle):
            case (str(), str()):
                return
            case (_, str()) | (str(), _):
                raise LengthMismatchError("select of self", "select of sqle")

        size_select_self = len(get_path(mdp_self))
        size_select_sqle = len(get_path(mdp_sqle))

        if size_select_self != size_select_sqle:
            raise LengthMismatchError("select of self", "select of sqle")

    def _check_legality_terminal_alter(self, cmd: Ctos) -> None:
        """
        Check if we can make a terminal or alter command compared to previous commands.

        Args:
            cmd: Command that we want to add to the command list.

        Raises:
            AlterError: If the command list already contains an alter command.
                self.flags.alter == True.
            TerminalError: If the command list already contains an terminal command.
                self.flags.terminal == True.
        """
        # HACK: The time that mypy supports the Strenum.
        # https://github.com/python/mypy/issues
        cmd = cast(Ct, cmd)

        if self.flags.terminal:
            raise TerminalError(cmd.value)
        if self.flags.alter:
            raise AlterError(cmd.value)

    def _check_legality(self, cmd: Ctos) -> None:
        """
        Check if we can make a command compared to previous commands.

        Args:
            cmd: Command that we want to add to the command list.

        Raises:
            AlterError: If the command list already contains an alter command.
                self.flags.alter == True
                or indirect raise by `_check_legality_terminal_alter`

            AlreadyExecutedError: If this SQLEnumerable is already executed.
                self.executed == True.

            GroupByWithJoinError: If the command is a group by
                and we already make a join.
                cmd == Ct.GROUP_BY and self.flags.join == True.

            MoreThanZeroError: If the command list isn't empty. len(self.cmd) > 0.

            NeedSelectError: If we make an intersect
                or union command with select before.
                self.flags.select == False.

            NoMaxOrMinAfterLimitOffsetError: If the command is type of max or min and
                we make a command who uses limit and/or offset before.
                cmd in [Ct.MAX, Ct.MIN] and self.flags.limit_offset == True.

            OneError: If we make a one command before. self.flags.one == True.

            OtherThanWhereError: If we make other than where command before.
                self._only_where_command() == False.

            SelectError: If we make a select before. self.flags.select == True.

            TerminalError: If the command list already contains an terminal command.
                self.flags.terminal == True
                or indirect raise by `_check_legality_terminal_alter`.

            UnknownCommandTypeError: If the command type is unknown. cmd not in Ct.
        """
        if self.executed:
            raise AlreadyExecutedError()
        if self.flags.one:
            raise OneError()

        # HACK: All following HACK it's just the time that mypy supports the Strenum.
        # https://github.com/python/mypy/issues

        match cmd:
            case Ct.SELECT:
                if self.flags.select:
                    cmd = cast(Ct, cmd)  # HACK
                    raise SelectError(cmd.value)
                if self.flags.alter:
                    cmd = cast(Ct, cmd)  # HACK
                    raise AlterError(cmd.value)
            case (Ct.INSERT | Ct.ALL | Ct.ANY | Ct.CONTAINS):
                if self.cmd:
                    cmd = cast(Ct, cmd)  # HACK
                    raise MoreThanZeroError(cmd.value)
            case (Ct.UPDATE | Ct.DELETE):
                if not self._only_where_command():
                    raise OtherThanWhereError()
            case Ct.WHERE:
                if self.flags.terminal:
                    cmd = cast(Ct, cmd)  # HACK
                    raise TerminalError(cmd.value)
            case (Ct.MAX | Ct.MIN):
                self._check_legality_terminal_alter(cmd)
                if self.flags.limit_offset:
                    cmd = cast(Ct, cmd)  # HACK
                    raise NoMaxOrMinAfterLimitOffsetError(cmd.value)
            case (Ct.INTERSECT | Ct.UNION):
                if not self.flags.select:
                    cmd = cast(Ct, cmd)  # HACK
                    raise NeedSelectError(cmd.value)
                self._check_legality_terminal_alter(cmd)
            case Ct.GROUP_BY:
                if self.flags.join:
                    raise GroupByWithJoinError()
                self._check_legality_terminal_alter(cmd)
            case cmd if cmd in list(Ct):  # type: ignore[operator] # HACK
                self._check_legality_terminal_alter(cmd)
            # The following case is just an other security layers,
            # but we can't go in this case for the moment.
            case _:  # pragma: no cover
                cmd = cast(Ct, cmd)  # HACK
                raise UnknownCommandTypeError(cmd.value)

    def _pre_build_for_count(
        self,
        include: List[Ctos],
        suffix: Command,
    ) -> SQLEnumerableData:
        """
        Build an SQLEnumerableData with the same attribute.

        Get the correct commands list to count the length of the return.

        Args:
            include: Commands we want to keep.
            suffix: Command added at the end.

        Returns:
            SQLEnumerableData with correct commands
        """
        commands = self.cmd
        pre_build_cmd = []

        for cmd in commands:
            if cmd.cmd_type in include:
                pre_build_cmd.append(cmd)

        if not pre_build_cmd:
            pre_build_cmd.append(Command(Ct.SELECT, DotMap(fquery=None)))

        pre_build_cmd.append(suffix)

        hidden_sqle = SQLEnumerableData(
            self.connection,
            self.flags.copy(),
            pre_build_cmd,
            self.table,
            None,
        )

        # limit_offset flag is false because we don't copy the limit_offset commands.
        hidden_sqle.flags.limit_offset = False

        # terminal flag is true because we add a count command (is a terminal command)
        hidden_sqle.flags.terminal = Terminal.COUNT

        return hidden_sqle

    def _set_count(self) -> None:
        """
        Set the count of a request's return in self.

        Raises:
            DeleteError: Indirect raise by `build`.
            LengthMismatchError: Indirect raise by `build`.
            NeedWhereError: Indirect raise by `build`.
            psycopg.Error: Indirect raise by `build`.
            TableError: Indirect raise by `build`.
            TooManyReturnValueError: Indirect raise by `build`.
            TypeError: Indirect raise by `build`.
            TypeOperatorError: Indirect raise by `build`.
            UnknownCommandTypeError: Indirect raise by `build`.
            ValueError: Indirect raise by `build`.
        """
        hidden_sqle = self._pre_build_for_count(
            [Ct.SELECT, Ct.WHERE, Ct.EXCEPT_],
            Command(Ct.COUNT, None),
        )

        cmd_to_execute = build(hidden_sqle)

        cursor = get_cursor(self.connection)
        cursor.execute(cmd_to_execute)
        fetch = cursor.fetchone()
        if fetch:
            count = fetch.count
        self.length = count

    def get_command(self) -> str | None:
        """
        Get the command as an str.

        Returns:
            The request as an str.

        Raises:
            DeleteError: Indirect raise by `build` or `_set_count`.
            LengthMismatchError: Indirect raise by `build` or `_set_count`.
            NeedWhereError: Indirect raise by `build` or `_set_count`.
            psycopg.Error: Indirect raise by `build` or `_set_count`.
            TableError: Indirect raise by `build` or `_set_count`.
            TooManyReturnValueError: Indirect raise by `build` or `_set_count`.
            TypeError: Indirect raise by `build` or `_set_count`.
            TypeOperatorError: Indirect raise by `build` or `_set_count`.
            UnknownCommandTypeError: Indirect raise by `build` or `_set_count`.
            ValueError: Indirect raise by `build` or `_set_count`.
        """
        if self.flags.limit_offset:
            self._set_count()
        hidden_sqle = SQLEnumerableData(
            self.connection,
            self.flags,
            self.cmd,
            self.table,
            self.length,
        )
        try:
            return build(hidden_sqle)
        except ReturnEmptyEnumerable:
            return None

    # ------------------------
    # |  Alteration methods  |
    # ------------------------

    def delete(
        self,
        fquery: LambdaMagicDotPath | None = None,
        *,
        armageddon: bool = False,
    ) -> SQLEnumerable:
        """
        Add a DELETE command to the command list.

        Args:
            fquery: Lambda function to get the element to delete.
            armageddon: True if you want to delete ALL your table, by default is False.

        Returns:
            Self.

        Raises:
            DeleteError: If we have an fquery and armageddon.
            ReadOnlyPermissionDeniedError: If we try to alter the database and the
                config is in readonly.
            AlterError: Indirect raise by `_check_legality` or `where`.
            AlreadyExecutedError: Indirect raise by `_check_legality` or `where`.
            OneError: Indirect raise by `_check_legality` or `where`.
            OtherThanWhereError: Indirect raise by `_check_legality` or `where`.
            TerminalError: Indirect raise by `_check_legality` or `where`.
        """
        if fquery and armageddon:
            raise DeleteError("predicate")

        # Can be test only with a config file and read_only = true,
        # but this feature is test in:
        # tests/algo/test_config.py with the test: test_readonly_true
        if is_read_only():  # pragma: no cover
            raise ReadOnlyPermissionDeniedError()

        self._check_legality(Ct.DELETE)
        self.flags.alter = True

        self.cmd.append(Command(Ct.DELETE, DotMap(armageddon=armageddon)))

        if fquery:
            self.where(fquery)

        return self

    def insert(
        self,
        column: List[str] | str,
        data: PyLinqSqlInsertType,
    ) -> SQLEnumerable:
        """
        Add an INSERT command to the command list.

        If data is a list, that means you make a multi insert.
        For more see: `docs/doc/examples/examples.md`
            or Usage.insert in the documentation.

        Args:
            column: Column where we want to insert.
            data: Data we want to insert.

        Returns:
            Self.

        Raises:
            ReadOnlyPermissionDeniedError: If we try to alter the database and the
                config is in readonly.
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            MoreThanZeroError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        # Can be test only with a config file and read_only = true,
        # but this feature is test in:
        # tests/algo/test_config.py with the test: test_readonly_true
        if is_read_only():  # pragma: no cover
            raise ReadOnlyPermissionDeniedError()

        self._check_legality(Ct.INSERT)
        self.flags.alter, self.flags.one = True, True

        self.cmd.append(Command(Ct.INSERT, DotMap(data=data, column=column)))

        return self

    def simple_insert(self, **kwargs: dict[str, Any]) -> SQLEnumerable:
        """
        Add an Insert command to the command list. Only for relationnal table.

        You give all column name with the name of kwargs and value in args.

        Args:
            **kwargs: All data and name of the column is the key in kwargs.

        Returns:
            Self.

        Raises:
            ReadOnlyPermissionDeniedError: Indirect raise by `self.insert`.
            AlterError: Indirect raise by `self.insert`.
            AlreadyExecutedError: Indirect raise by `self.insert`.
            MoreThanZeroError: Indirect raise by `self.insert`.
            OneError: Indirect raise by `self.insert`.
            TerminalError: Indirect raise by `self.insert`.
        """
        return self.insert(column=list(kwargs.keys()), data=tuple(kwargs.values()))

    def update(self, fquery: Callable[[MagicDotPath], MagicDotPath]) -> SQLEnumerable:
        """
        Add an UPDATE command to the command list.

        Args:
            fquery: Lambda function to get path of the modification.

        Returns:
            Self.

        Raises:
            ReadOnlyPermissionDeniedError: If we try to alter the database and the
                config is in readonly.
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            OtherThanWhereError: Indirect raise by `_check_legality`.
            ReadOnlyPermissionDeniedError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        # Can be test only with a config file and read_only = true,
        # but this feature is test in:
        # tests/algo/test_config.py with the test: test_readonly_true
        if is_read_only():  # pragma: no cover
            raise ReadOnlyPermissionDeniedError()

        self._check_legality(Ct.UPDATE)
        self.flags.alter = True

        self.cmd.append(Command(Ct.UPDATE, DotMap(fquery=fquery)))

        return self

    # -------------------
    # |  Select method  |
    # -------------------

    def select(self, fquery: LambdaMagicDotPath | None = None) -> SQLEnumerable:
        """
        Add an SELECT command to the command list.

        Args:
            fquery: Lambda function to get path(s) of selection. Its optional.
                By default it's None for a request "SELECT *"

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            SelectError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.SELECT)

        self.flags.select = True

        self.cmd.append(Command(Ct.SELECT, DotMap(fquery=fquery)))

        return self

    # -----------------
    # |  One methods  |
    # -----------------

    def contains(
        self,
        fquery: Dict[str, Any] | Callable[[MagicDotPath], MagicDotPath],
    ) -> SQLEnumerable:
        """
        Add an CONTAINS command to the command list.

        Args:
            fquery: Rawdata or path(s).

        - Rawdata: Entire line of a table to know if the table contains this line.

        - Path(s): Lambda function to get path(s) to know if a line of the table
            contains this.

        Returns:
            Self.

        Raises:
            EmptyInputError: If fquery is a dict and is empty.
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            MoreThanZeroError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.CONTAINS)

        if isinstance(fquery, dict) and not fquery:
            raise EmptyInputError("contains")

        self.flags.one = True

        self.cmd.append(Command(Ct.CONTAINS, DotMap(fquery=fquery)))

        return self

    def all(self, fquery: Callable[[MagicDotPath], MagicDotPath]) -> SQLEnumerable:
        """
        Add an ALL command to the command list.

        Args:
            fquery: Lambda function to give the predicate.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            MoreThanZeroError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.ALL)

        self.flags.one = True

        self.cmd.append(Command(Ct.ALL, DotMap(fquery=fquery)))

        return self

    def any(
        self,
        fquery: Callable[[MagicDotPath], MagicDotPath] | None = None,
    ) -> SQLEnumerable:
        """
        Add an ANY command to the command list.

        Args:
            fquery: Lambda function to give the predicate. Its optional.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            MoreThanZeroError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.ANY)

        self.flags.one = True

        self.cmd.append(Command(Ct.ANY, DotMap(fquery=fquery)))

        return self

    # ----------------------
    # |  Terminal methods  |
    # ----------------------

    def count(self) -> SQLEnumerable:
        """
        Add a COUNT command to the command list.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.COUNT)

        self.flags.terminal = Terminal.COUNT

        self.cmd.append(Command(Ct.COUNT, None))

        return self

    def distinct(self) -> SQLEnumerable:
        """
        Add a DISTINCT command to the command list.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.

            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.DISTINCT)

        self.flags.terminal = Terminal.DISTINCT

        self.cmd.append(Command(Ct.DISTINCT, None))

        return self

    def element_at(self, index: int) -> SQLEnumerable:
        """
        Add an ELEMENT_AT command to the command list.

        Args:
            index: Index of element we want. Must be a positive number.
                Index must be strictly inferior than any other `take` call previously.

        Returns:
            Self.

        Raises:
            IndexError: If we make a `take(n)` before and index >= n.
            AlterError: Indirect raise by `_check_legality`, `skip` or `take`.
            AlreadyExecutedError: Indirect raise by `_check_legality`, `skip`
                or `take`.
            NegativeNumberError: Indirect raise by `skip` or `take`.
            OneError: Indirect raise by `_check_legality`, `skip` or `take`.
            SelectError: Indirect raise by `_check_legality`, `skip` or `take`.
            TerminalError: Indirect raise by `_check_legality`, `skip` or `take`.
        """
        commands = self.cmd
        for cmd in commands:
            if cmd.cmd_type == Ct.TAKE and index >= cmd.args.number:
                raise IndexError()

        self.skip(index).take(1)
        self.flags.terminal = Terminal.ELEMENT_AT
        return self

    def element_at_or_default(self, index: int) -> SQLEnumerable:
        """
        Add an ELEMENT_AT_OR_DEFAULT command to the command list.

        Args:
            index: Index of element we want. Must be a positive number.
                Index must be strictly inferior than any other `take` call previously.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `element_at`.
            AlreadyExecutedError: Indirect raise by `element_at`.
            IndexError: Indirect raise by `element_at`.
            NegativeNumberError: Indirect raise by `element_at`.
            OneError: Indirect raise by `element_at`.
            SelectError: Indirect raise by `element_at`.
            TerminalError: Indirect raise by `element_at`.
        """
        self.flags.default_cmd = True
        return self.element_at(index)

    def except_(self, exclude: SQLEnumerable) -> SQLEnumerable:
        """
        Add an EXCEPT command to the command list.

        Args:
            exclude: SQLEnumerable to give the exclude predicate.

        Returns:
            Self.
        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            LengthMismatchError: Indirect raise by `get_command`.
            NeedWhereError: Indirect raise by `get_command`.
            OneError: Indirect raise by `_check_legality`.
            psycopg.Error: Indirect raise by `get_command`.
            TableError: Indirect raise by `get_command`.
            TerminalError: Indirect raise by `_check_legality`.
            TooManyReturnValueError: Indirect raise by `get_command`.
            TypeError: Indirect raise by `get_command`.
            TypeOperatorError: Indirect raise by `get_command`.
            ValueError: Indirect raise by `get_command`.
        """
        self._check_legality(Ct.EXCEPT_)

        try:
            self._check_select(exclude, "except")
        except NeedSelectError:
            pass

        self.flags.terminal = Terminal.EXCEPT_

        exclude_cmd = exclude.get_command()

        self.cmd.append(Command(Ct.EXCEPT_, DotMap(exclude_cmd=exclude_cmd)))

        return self

    def first(self, fquery: LambdaMagicDotPath | None = None) -> SQLEnumerable:
        """
        Add a FIRST command to the command list.

        Args:
            fquery: Lambda function to give the predicate. Its optional.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `element_at` or `where`.
            AlreadyExecutedError: Indirect raise by `element_at` or `where`.
            NegativeNumberError: Indirect raise by `element_at`.
            OneError: Indirect raise by `element_at` or `where`.
            SelectError: Indirect raise by `element_at` or `where`.
            TerminalError: Indirect raise by `element_at` or `where`.
        """
        if fquery:
            self.where(fquery)

        # element_at can be raise NegativeError but never with index == 0.
        self.element_at(0)

        return self

    def first_or_default(
        self,
        fquery: LambdaMagicDotPath | None = None,
    ) -> SQLEnumerable:
        """
        Add a FIRST_OR_DEFAULT command to the command list.

        Args:
            fquery: Lambda function to give the predicate. Its optional.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `first`.
            AlreadyExecutedError: Indirect raise by `first`.
            NegativeNumberError: Indirect raise by `first`.
            OneError: Indirect raise by `first`.
            SelectError: Indirect raise by `first`.
            TerminalError: Indirect raise by `first`.
        """
        self.flags.default_cmd = True
        return self.first(fquery)

    def group_by(
        self,
        by_fquery: LambdaMagicDotPath,
        aggreg_fquery: LambdaMagicDotPathAggregate,
    ) -> SQLEnumerable:
        """
        Add a GROUP_BY command to the command list.

        Args:
            by_fquery: lambda function to give the selection.
            aggreg_fquery: lambda function to give the aggregation.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality` or `select`.
            AlreadyExecutedError: Indirect raise by `_check_legality` or `select`.
            GroupByWithJoinError: Indirect raise by `_check_legality` or `select`.
            OneError: Indirect raise by `_check_legality` or `select`.
            SelectError: Indirect raise by `_check_legality` or `select`.
            TerminalError: Indirect raise by `_check_legality` or `select`.
        """
        self._check_legality(Ct.GROUP_BY)

        self.select(by_fquery)

        self.flags.terminal = Terminal.GROUP_BY

        self.cmd.append(
            Command(
                Ct.GROUP_BY,
                DotMap(
                    aggreg_fquery=aggreg_fquery,
                ),
            ),
        )

        return self

    def intersect(self, sqle: SQLEnumerable) -> SQLEnumerable:
        """
        Add an INTERSECT command to the command list.

        Args:
            sqle: An other SQLEnumerable to make the intersection.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            DeleteError: Indirect raise by `build`.
            LengthMismatchError: Indirect raise by `build`.
            NeedSelectError: Indirect raise by `_check_legality`.
            NeedWhereError: Indirect raise by `build`.
            OneError: Indirect raise by `_check_legality`.
            psycopg.Error: Indirect raise by `build`.
            TableError: Indirect raise by `build`.
            TerminalError: Indirect raise by `_check_legality`.
            TooManyReturnValueError: Indirect raise by `build`.
            TypeError: Indirect raise by `build`.
            TypeOperatorError: Indirect raise by `build`.
            ValueError: Indirect raise by `build`.
        """
        self._check_legality(Ct.INTERSECT)

        self._check_select(sqle, "intersect")

        sqle_data = SQLEnumerableData(
            sqle.connection,
            sqle.flags,
            sqle.cmd,
            sqle.table,
            sqle.length,
        )

        built_sqle_2 = build(sqle_data)

        self.flags.terminal = Terminal.INTERSECT

        self.cmd.append(Command(Ct.INTERSECT, DotMap(built_sqle_2=built_sqle_2)))

        return self

    def last(self, fquery: LambdaMagicDotPath | None = None) -> SQLEnumerable:
        """
        Add a LAST command to the command list.

        Args:
            fquery: Lambda function to give the predicate. Its optional.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`, `where` or `take_last`.
            AlreadyExecutedError: Indirect raise by `_check_legality`, `where`
                or `take_last`.
                or `take_last`.
            OneError: Indirect raise by `_check_legality`, `where` or `take_last`.
                or `take_last`.
            SelectError: Indirect raise by `_check_legality`, `where` or `take_last`.
            TerminalError: Indirect raise by `_check_legality`, `where` or `take_last`.
        """
        self._check_legality(Ct.LAST)

        if fquery:
            self.where(fquery)

        # `take_last` can raise NegativeNumberError
        # but not here because wa always call take_last with 1.
        self.take_last(1)

        self.flags.terminal = Terminal.LAST

        return self

    def last_or_default(
        self,
        fquery: LambdaMagicDotPath | None = None,
    ) -> SQLEnumerable:
        """
        Add a LAST_OR_DEFAULT command to the command list.

        Args:
            fquery: Lambda function to give the predicate. Its optional.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `last`.
            AlreadyExecutedError: Indirect raise by `last`.
            OneError: Indirect raise by `last`.
            SelectError: Indirect raise by `last`.
            TerminalError: Indirect raise by `last`.
        """
        self.flags.default_cmd = True
        return self.last(fquery)

    def max(
        self,
        fquery: LambdaMagicDotPath | None,
        cast_type: type | None = None,
    ) -> SQLEnumerable:
        """
        Add a MAX command to the command list.

        Args:
            fquery: Lambda function to get the path(s) of the selection.
            cast_type: Type in which we want to cast the path(s). Its optional.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            NoMaxOrMinAfterLimitOffsetError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.

            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.MAX)

        self.flags.terminal = Terminal.MAX

        self.cmd.append(Command(Ct.MAX, DotMap(fquery=fquery, cast_type=cast_type)))

        return self

    def min(
        self,
        fquery: LambdaMagicDotPath | None,
        cast_type: type | None = None,
    ) -> SQLEnumerable:
        """
        Add a MIN command to the command list.

        Args:
            fquery: Lambda function to get the path(s) of the selection.
            cast_type: Type in which we want to cast the path(s). Its optional.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            NoMaxOrMinAfterLimitOffsetError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.

            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.MIN)

        self.flags.terminal = Terminal.MIN

        self.cmd.append(Command(Ct.MIN, DotMap(fquery=fquery, cast_type=cast_type)))

        return self

    def single(self, fquery: LambdaMagicDotPath | None = None) -> SQLEnumerable:
        """
        Add a SINGLE command to the command list.

        Args:
            fquery: Lambda function to give the predicate. Its optional.

        Returns:
            Self.

        Raises:
            DeleteError: If we have an fquery and armageddon.
            AlterError: Indirect raise by `_check_legality` or `where`.
            AlreadyExecutedError: Indirect raise by `_check_legality` or `where`.
            OneError: Indirect raise by `_check_legality` or `where`.
            SelectError: Indirect raise by `_check_legality` or `where`.
            TerminalError: Indirect raise by `_check_legality` or `where`.
        """
        self._check_legality(Ct.SINGLE)

        if fquery:
            self.where(fquery)

        self.flags.terminal = Terminal.SINGLE

        return self

    def single_or_default(
        self,
        fquery: LambdaMagicDotPath | None = None,
    ) -> SQLEnumerable:
        """
        Add a SINGLE_OR_DEFAULT command to the command list.

        Args:
            fquery: Lambda function to give the predicate. Its optional.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `single`.
            AlreadyExecutedError: Indirect raise by `single`.
            OneError: Indirect raise by `single`.
            SelectError: Indirect raise by `single`.
            TerminalError: Indirect raise by `single`.
        """
        self.flags.default_cmd = True
        return self.single(fquery)

    def union(self, sqle: SQLEnumerable, all_: bool = False) -> SQLEnumerable:
        """
        Add an UNION command to the command list.

        Args:
            sqle: An other SQLEnumerable to make the union.
            all_: Boolean to know if we want an UNION (False) or an UNION ALL (True).
                By default: False.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            DeleteError: Indirect raise by `build`.
            LengthMismatchError: Indirect raise by `build`.
            NeedSelectError: Indirect raise by `_check_legality`.
            NeedWhereError: Indirect raise by `build`.
            OneError: Indirect raise by `_check_legality`.
            psycopg.Error: Indirect raise by `build`.
            TableError: Indirect raise by `build`.
            TerminalError: Indirect raise by `_check_legality`.
            TooManyReturnValueError: Indirect raise by `build`.
            TypeError: Indirect raise by `build`.
            TypeOperatorError: Indirect raise by `build`.
            ValueError: Indirect raise by `build`.
        """
        self._check_legality(Ct.UNION)
        self._check_select(sqle, "intersect")

        sqle_data = SQLEnumerableData(
            sqle.connection,
            sqle.flags,
            sqle.cmd,
            sqle.table,
            sqle.length,
        )

        built_sqle_2 = build(sqle_data)

        self.flags.terminal = Terminal.UNION

        self.cmd.append(Command(Ct.UNION, DotMap(built_sqle_2=built_sqle_2, all_=all_)))

        return self

    # ---------------------
    # |  Context methods  |
    # ---------------------

    def group_join(  # pylint: disable=too-many-arguments
        self,
        inner: SQLEnumerable,
        outer_key: LambdaMagicDotPath,
        inner_key: LambdaMagicDotPath,
        result_function: LambdaMagicDotPathAggregate,
        join_type: JoinType = JoinType.INNER,
    ) -> SQLEnumerable:
        """
        Add a GROUP JOIN command to the command list.

        Warning: For the moment you need to put inner before outer in the lambda

        for example, if inner is satellite in the result function you need to make
        lambda satellite, objects: stalellite.x.y, objects.a.b

        Args:
            inner: SQLEnumerable with which we want to make the join.
            outer_key: Lambda function to get the path(s) parameters
                for comparison in the outer SQLEnumerable.
            inner_key: Lambda function to get the path(s) parameters
                for comparison in the inner SQLEnumerable.
            result_function: Lambda function to get the path(s) for the selection.
            join_type: Type of join.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.GROUP_JOIN)

        outer = SQLEnumerableData(
            self.connection,
            self.flags,
            self.cmd,
            self.table,
            self.length,
        )
        inner_sqled = SQLEnumerableData(
            inner.connection,
            inner.flags,
            inner.cmd,
            inner.table,
            self.length,
        )

        self.flags.select, self.flags.join = True, True

        self.cmd.append(
            Command(
                Ct.GROUP_JOIN,
                DotMap(
                    outer=outer,
                    inner=inner_sqled,
                    outer_key=outer_key,
                    inner_key=inner_key,
                    result_function=result_function,
                    join_type=join_type,
                ),
            ),
        )

        return self

    def join(  # pylint: disable=too-many-arguments
        self,
        inner: SQLEnumerable,
        outer_key: LambdaMagicDotPath,
        inner_key: LambdaMagicDotPath,
        result_function: LambdaMagicDotPath | None = None,
        join_type: JoinType = JoinType.INNER,
    ) -> SQLEnumerable:
        """
        Add a JOIN command to the command list.

        Warning: For the moment you need to put inner before outer in the lambda

        for example, if inner is satellite in the result function you need to make
        lambda satellite, objects: stalellite.x.y, objects.a.b

        Args:
            inner: SQLEnumerable with which we want to make the join.
            outer_key: Lambda function to get the path(s) parameters
                for comparison in the outer SQLEnumerable.
            inner_key: Lambda function to get the path(s) parameters
                for comparison in the inner SQLEnumerable.
            result_function: Lambda function to get the path(s) for the selection.
            join_type: Type of join.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            GroupByWithJoinError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.JOIN)

        outer = SQLEnumerableData(
            self.connection,
            self.flags,
            self.cmd,
            self.table,
            self.length,
        )
        inner_sqled = SQLEnumerableData(
            inner.connection,
            inner.flags,
            inner.cmd,
            inner.table,
            self.length,
        )

        self.flags.select, self.flags.join = True, True

        self.cmd.append(
            Command(
                Ct.JOIN,
                DotMap(
                    outer=outer,
                    inner=inner_sqled,
                    outer_key=outer_key,
                    inner_key=inner_key,
                    result_function=result_function,
                    join_type=join_type,
                ),
            ),
        )

        return self

    def order_by(self, fquery: LambdaMagicDotPath) -> SQLEnumerable:
        """
        Add an ORDER_BY command to the command list.

        Args:
            fquery: Lambda function to get the path(s) for the ordering.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.ORDER_BY)

        self.cmd.append(Command(Ct.ORDER_BY, DotMap(fquery=fquery)))
        return self

    def order_by_descending(self, fquery: LambdaMagicDotPath) -> SQLEnumerable:
        """
        Add an ORDER_BY_DESCENDING command to the command list.

        Args:
            fquery: Lambda function to get the path(s) for the ordering.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.ORDER_BY_DESC)

        self.cmd.append(Command(Ct.ORDER_BY_DESC, DotMap(fquery=fquery)))
        return self

    def skip(self, number: int) -> SQLEnumerable:
        """
        Add an SKIP command to the command list.

        Args:
            number: Number of element to skip.

        Returns:
            Self.

        Raises:
            NegativeNumberError: If number < 0.
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        if number < 0:
            raise NegativeNumberError()

        self._check_legality(Ct.SKIP)

        self.flags.limit_offset = True

        self.cmd.append(Command(Ct.SKIP, DotMap(number=number)))

        return self

    def skip_last(self, number: int) -> SQLEnumerable:
        """
        Add an SKIP_LAST command to the command list.

        Args:
            number: Number of element to skip the end.

        Returns:
            Self.

        Raises:
            NegativeNumberError: If number < 0.
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        if number < 0:
            raise NegativeNumberError()

        self._check_legality(Ct.SKIP_LAST)

        self.flags.limit_offset = True

        self.cmd.append(Command(Ct.SKIP_LAST, DotMap(number=number)))

        return self

    def take(self, number: int) -> SQLEnumerable:
        """
        Add an TAKE command to the command list.

        Args:
            number: Number of element to take.

        Returns:
            Self.

        Raises:
            NegativeNumberError: If number < 0.
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        if number < 0:
            raise NegativeNumberError()

        self._check_legality(Ct.TAKE)

        self.flags.limit_offset = True

        self.cmd.append(Command(Ct.TAKE, DotMap(number=number)))

        return self

    def take_last(self, number: int) -> SQLEnumerable:
        """
        Add an TAKE_LAST command to the command list.

        Args:
            number: Number of element to take.

        Returns:
            Self.

        Raises:
            NegativeNumberError: If number < 0.
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        if number < 0:
            raise NegativeNumberError()

        self._check_legality(Ct.TAKE_LAST)

        self.flags.limit_offset = True

        self.cmd.append(Command(Ct.TAKE_LAST, DotMap(number=number)))

        return self

    def where(self, fquery: LambdaMagicDotPath) -> SQLEnumerable:
        """
        Add an WHERE command to the command list.

        Args:
            fquery: Lambda function the get the path of the predicate.

        Returns:
            Self.

        Raises:
            AlterError: Indirect raise by `_check_legality`.
            AlreadyExecutedError: Indirect raise by `_check_legality`.
            OneError: Indirect raise by `_check_legality`.
            TerminalError: Indirect raise by `_check_legality`.
        """
        self._check_legality(Ct.WHERE)

        self.cmd.append(Command(Ct.WHERE, DotMap(fquery=fquery)))

        return self

    def select_many(self) -> None:
        """
        Generate a SELECT MANY request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def to_list(self) -> None:
        """
        Generate a TO LIST request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def median(self) -> None:
        """
        Generate a MEDIAN request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def aggregate(self) -> None:
        """
        Generate a AGGREGATE request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def append(self) -> None:
        """
        Generate a APPEND request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def prepend(self) -> None:
        """
        Generate a PREPEND request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def empty(self) -> None:
        """
        Generate a EMPTY request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def range(self) -> None:
        """
        Generate a RANGE request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def repeat(self) -> None:
        """
        Generate a REPEAT request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def reverse(self) -> None:
        """
        Generate a REVERSE request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def skip_while(self) -> None:
        """
        Generate a SKIP WHILE request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def take_while(self) -> None:
        """
        Generate a TAKE WHILE request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def zip(self) -> None:
        """
        Generate a ZIP request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def default_if_empty(self) -> None:
        """
        Generate a DEFAULT IF EMPTY request.

        Raises:
            NotImplementedError: Because it's functions is not implemented.
        """
        raise NotImplementedError()

    def execute(self) -> Enumerable | int | tuple | bool:
        """
        Execute the request.

        Returns:
            Result of the execution. Can be an Enumerable, int, dict or boolean.

        Raises:
            AlreadyExecutedError: If this SQLEnumerable is already executed.
            ActionError: If we don't make a `select`, an alter or a one command.
            IndexError: If we make an `element_at` but not by default
                and the command to execute is None.
            EmptyQueryError: If cmd to execute is empty or Indirect raise by
                `execute_select`, `execute_alter` or `execute_one`.
            CursorCloseError: Indirect raise by
                `execute_select`, `execute_alter` or `execute_one`.
            DatabError: Indirect raise by `execute_select`.
            DeleteError: Indirect raise by `get_command`.
            EmptyRecord: Indirect raise by `execute_select`.
            FetchError: Indirect raise by `execute_select`.
            LengthMismatchError: Indirect raise by `get_command`.
            NeedWhereError: Indirect raise by `get_command`.
            psycopg.Error: Indirect raise by `get_command`.
            TableError: Indirect raise by `get_command`.
            TooManyReturnValueError: Indirect raise by `get_command`.
            TypeError: Indirect raise by `get_command`.
            TypeOperatorError: Indirect raise by `get_command`.
            ValueError: Indirect raise by `get_command`.
        """
        if self.executed:
            raise AlreadyExecutedError()

        if not self.flags.select and not self.flags.alter and not self.flags.one:
            raise ActionError()
        cmd_to_execute = self.get_command()
        if not cmd_to_execute:
            match (
                self.flags.default_cmd,
                self.flags.terminal,
                self.flags.limit_offset,
            ):
                case (True, _, _):
                    return None
                case (False, Terminal.ELEMENT_AT, _):
                    raise IndexError() from ReturnEmptyEnumerable
                case (_, _, True):
                    return Enumerable.empty()
                case _:
                    # pylint disable=duplicate-code
                    raise EmptyQueryError(
                        ProgrammingError(),
                        cmd_to_execute,
                        "We can't execute empty request",
                        False,
                    ) from ProgrammingError
                    # pylint enable=duplicate-code

        hidden_sqle = SQLEnumerableData(
            self.connection,
            self.flags,
            self.cmd,
            self.table,
            self.length,
        )
        if self.flags.select:
            record = execute_select(cmd_to_execute, hidden_sqle)
        elif self.flags.alter:
            record = execute_alter(cmd_to_execute, hidden_sqle)
        elif self.flags.one:
            record = execute_one(cmd_to_execute, hidden_sqle)

        self.executed = True
        return record
