"""All exceptions for the project py_linq_sql."""


# -------------
# |  WARNING  |
# -------------
class ReturnEmptyEnumerable(Warning):
    """Raised when we get an empty enumerable in the record."""


# ------------
# |  ERRORS  |
# ------------
class PyLinqSQLError(Exception):
    """Base exception for the project."""


# -------------------------
# |  PSQLConnectionError  |
# -------------------------
class PSQLConnectionError(PyLinqSQLError):
    """Error raised if we can't connect to a database."""


# -------------------------------
# |  CONFIG PERMISSIONS ERRORS  |
# -------------------------------
class ConfigPermissionError(PyLinqSQLError):
    """Error raised if you does not have permission to access to something."""


class TablePermissionDeniedError(ConfigPermissionError):
    """Raised when a table is not accessible according to the black and white lists."""

    def __init__(self, table: str) -> None:
        """Initialize a PermissionDeniedError."""
        super().__init__(
            f"Permission Denied for the table {table}. "
            "Check your white and black lists.",
        )


class ReadOnlyPermissionDeniedError(ConfigPermissionError):
    """Raised when a table is not accessible according to the black and white lists."""

    def __init__(self) -> None:
        """Initialize a PermissionDeniedError."""
        super().__init__(
            "Permission Denied write to the database. "
            "Check your read only configuration.",
        )


# ------------------
# |  INPUT ERRORS  |
# ------------------
class InputError(PyLinqSQLError):
    """Error raised if input argument is invalid."""


class ColumnNameError(InputError):
    """Raised when a custom column name is not in the good format."""

    def __init__(self, name: str) -> None:
        """Initialize a ColumnNameError."""
        super().__init__(
            f"The column name '{name}' isn't a valid column name. "
            "A valid column name begin by a letter and is followed by "
            "letter, number or '_'. The max size is 58 bytes. "
            "The max size of a column name is 63 bytes for the database. "
            "But here we limit it to 58 bytes "
            "because we keep 1 bytes for a potential prefix of psql "
            "and 4 bytes for a suffix if there are several identical column names.",
        )


class NegativeNumberError(ArithmeticError, InputError):
    """
    Error raised when we try to pass a negative number to a function.

    If this function accepts only positive numbers.
    """

    def __init__(self) -> None:
        """Initialize a NegativeNumberError."""
        super().__init__("numbers must be positive.")


class TableError(InputError):
    """Raised when we try to reference a table not selected after a join."""

    def __init__(self, table: str, good_tables: list[str]) -> None:
        """Initialize a TableError."""
        super().__init__(
            "You try to make a command after a join. When you do that you must "
            "give the table EXPLICITLY in the lambda.\n"
            "Example:\n"
            "\t.where(lambda x: x.satellite.data.name)\n"
            f"Here you have referred to {table} while the tables to select in the join "
            f"are {good_tables}.\n",
        )


class TypeOperatorError(InputError, TypeError):
    """Error raised when we try to cast a value in a unknown type."""

    def __init__(self, expected: list[type], actual: type) -> None:
        """Initialize a TypeOperatorError."""
        super().__init__(
            f"Wrong type, only :\n" f"{expected} " f"can be used here. Not {actual}.",
        )


# --------------------------
# |  PRE EXECUTION ERRORS  |
# --------------------------
class PreExecutionError(PyLinqSQLError):
    """Error raised when we can't prepare the execution."""


class ActionError(PreExecutionError):
    """Error raised when we try to execute a request without action."""

    def __init__(self) -> None:
        """Initialize an ActionError."""
        super().__init__(
            "You have to make an action command before execute an SQLEnumerable.",
        )


class EmptyInputError(PreExecutionError):
    """Error raised when we try to call a command with an empty argument."""

    def __init__(self, name_of_cmd: str) -> None:
        """Initialize an EmptyInputError."""
        super().__init__(f"Input in {name_of_cmd} are empty.")


class EmptyRecordError(PreExecutionError):
    """Error raised when the record of a request is empty."""

    def __init__(self) -> None:
        """Initialize an EmptyRecordError."""
        super().__init__("Record are None.")


# ------------------
# |  BUILD ERRORS  |
# ------------------
class BuildError(PyLinqSQLError):
    """Error raised when something wrong when we build the request."""


class DeleteError(PyLinqSQLError):
    """Raised when we try to make a delete with a predicate and armageddon == True."""

    def __init__(self, other_cmd: str) -> None:
        """Initialize a DeleteError."""
        super().__init__(
            "You can't make a delete with "
            f"a {other_cmd} and armageddon set at True. You need to choose.",
        )


class LengthMismatchError(PyLinqSQLError):
    """Error raised when length of lambda are not equal."""

    def __init__(self, *args: str) -> None:
        """Initialize a LengthMismatchError."""
        msg = "Size of "
        for idx, _input in enumerate(args):
            msg += _input
            if not idx == len(args) - 1:
                msg += ", "
        msg += " are not equal"
        super().__init__(msg)


class NeedWhereError(PyLinqSQLError):
    """Raised when we try to make a delete without armageddon and without where."""

    def __init__(self) -> None:
        """Initialize a NeedWhereError."""
        super().__init__(
            "You need to make a where before or after delete "
            "or give a predicate to delete if you don't use "
            "the parameter `armageddon` to say 'I want to delete all my table'.",
        )


class TooManyReturnValueError(TypeError, PyLinqSQLError):
    """Error raised when we pass to many value to a MagicDotPaths."""

    def __init__(self, name: str) -> None:
        """Initialize a TooManyReturnValueError."""
        super().__init__(f"{name} take only one lambda, only one modification.")


# ----------------------
# |  EXECUTION ERRORS  |
# ----------------------
class ExecutionError(PyLinqSQLError):
    """Error raised if we can't execute a request."""

    def __init__(
        self,
        err: Exception,
        command: str | None,
        context: str,
        executed: bool,
    ) -> None:
        """Initialize an ExecutionError."""
        exec_ = "wasn't" if not executed else "was"
        super().__init__(
            f"The command {command} "
            f"{exec_} executed.\n"
            f"Context : {context}.\n"
            "An exception has occurred: "
            f"{err.__str__()}\n"
            f"Exception TYPE: {type(err)}\n",
        )


class CursorCloseError(ExecutionError):
    """Error raised when we try to close a cursor already close.."""


class DatabError(ExecutionError):
    """Error raised when something wrong with the database."""


class EmptyQueryError(ExecutionError):
    """Error raised when we try to execute a empty query."""


class FetchError(ExecutionError):
    """Error raised when we can't fetch the record of an execution."""


# ---------------------
# |  LEGALITY ERRORS  |
# ---------------------
class LegalityError(PyLinqSQLError):
    """Error raised when we does not respect the legality rules."""


class AlreadyExecutedError(LegalityError):
    """Raised when we try use an SQLEnumerable who has been already executed."""

    def __init__(self) -> None:
        """Initialize an AlreadyExecutedError."""
        super().__init__(
            "You can't re use an SQL_Enumerable who has been already executed.",
        )


class AlterError(LegalityError):
    """Error raised when we try to make a action command after a alter command."""

    def __init__(self, self_name: str) -> None:
        """Initialize an AlterError."""
        super().__init__(f"You can't make {self_name} after an alter command.")


class GroupByWithJoinError(LegalityError):
    """Raised when we try to make a group by after a join."""

    def __init__(self) -> None:
        """Initialize a GroupByWithJoinError."""
        super().__init__("You can't make a group_by after a join, use group_join().")


class MoreThanZeroError(LegalityError):
    """Error raised when we make command who must be alone and this isn't the case."""

    def __init__(self, name_of_cmd: str) -> None:
        """Initialize a MoreThanZeroError."""
        super().__init__(f"You can't make {name_of_cmd} command after other command.")


class NeedSelectError(LegalityError):
    """Raised when we try to make a command who need a select and we don't have it."""

    def __init__(self, cmd_name: str) -> None:
        """Initialize a NeedSelectError."""
        super().__init__(f"All SQLEnumerable in {cmd_name} must be a SELECT request.")


class NoMaxOrMinAfterLimitOffsetError(LegalityError):
    """
    Error when we try to make a max or a min after a limit offset command.

    In SQL MAX and MIN return only one element it's useless to make take or skip after.
    If we want take only 4 elements in the table and get the max we can make the max
    (or min) after the execution with Enumerable.max().

    If we our `take()` takes a very large number and we want the max
    to be executed by the server we must execute an explicit nested fquery.

    Examples:
        With a not too big `take()`:
        >>> record = SQLEnumerable(con, table).take(183).execute() # doctest: +SKIP
        >>> record.max(lambda x: x["mass"]) # doctest: +SKIP

        With a large `take()`:
        >>> sqle_1 = SQLEnumerable(con, table).take(4691) # doctest: +SKIP
        >>> record = ( # doctest: +SKIP
        ...     SQLEnumerable(con, sqle_1) # doctest: +SKIP
        ...    .max(lambda x: x.mass) # doctest: +SKIP
        ...    .execute() # doctest: +SKIP
        ... ) # doctest: +SKIP
    """

    def __init__(self, cmd_name: str) -> None:
        """Initialize a NoMaxOrMinAfterLimitOffsetError."""
        super().__init__(f"You can't make {cmd_name} after a limit or offset.")


class OneError(LegalityError):
    """Error raised when we try to make a command after a one command."""

    def __init__(self) -> None:
        """Initialize a OneError."""
        super().__init__("You can't make command after one commands.")


class OtherThanWhereError(LegalityError):
    """
    Error raised when we get commands other than where.

    For functions who only accepts where commands.
    """

    def __init__(self) -> None:
        """Initialize an OtherThanWhereError."""
        super().__init__("Other than where commands in list of commands.")


class SelectError(LegalityError):
    """Error raised when we try to make a action command after a select command."""

    def __init__(self, self_name: str) -> None:
        """Initialize a SelectError."""
        super().__init__(f"You can't make {self_name} after select.")


class TerminalError(LegalityError):
    """Error raised when we try to make a command after a terminal command."""

    def __init__(self, name_of_cmd: str) -> None:
        """Initialize a TerminalError."""
        super().__init__(
            f"You can't make {name_of_cmd} command after a terminal command.",
        )


# -----------------------------
# |  UnknownCommandTypeError  |
# -----------------------------
class UnknownCommandTypeError(TypeError, PyLinqSQLError):
    """Error raised when we try to build an unknown command."""

    # The following case is just an other security layers,
    # but we can't go in this case for the moment.
    def __init__(self, cmd_type: str) -> None:  # pragma: no cover
        """Initialize an UnknownError."""
        super().__init__(f"Unknown command type : {cmd_type}")
