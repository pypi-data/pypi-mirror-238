"""Execute request for an SQLEnumerable."""
# Standard imports
import logging

# Third party imports
from psycopg import Cursor, DatabaseError, InterfaceError, ProgrammingError, sql
from psycopg.errors import (
    InvalidRowCountInLimitClause,
    InvalidRowCountInResultOffsetClause,
)
from py_linq import Enumerable

# Local imports
from ..exception.exception import (
    CursorCloseError,
    DatabError,
    EmptyQueryError,
    EmptyRecordError,
    FetchError,
)
from .classes.enum import CommandType, Terminal
from .classes.other_classes import SQLEnumerableData
from .db import get_cursor

logg = logging.getLogger(__name__)


def _fetch_enumerable(
    sqle: SQLEnumerableData,
    cursor: Cursor,
    cmd_to_execute: str,
) -> Enumerable:
    """
    Fetch a cursor to get an Enumerable.

    Args:
        cmd_to_execute:Command which was executed.

    Returns:
        A Enumerable with record.

    Raises:
        CursorCloseError: If the cursor is already close. We proceed to a rollback.
        FetchError: If we have an error when fetching the cursor.
    """
    try:
        record = cursor.fetchall()
    # For the moment I can't reproduce the error, but the test exists in:
    # tests/exceptions/test_execute.py.
    except ProgrammingError as err:  # pragma: no cover
        cursor.close()
        if sqle.connection:
            sqle.connection.rollback()
        raise FetchError(
            err,
            cmd_to_execute,
            "But an error was caught in the data recovery. We proceed to a rollback",
            True,
        ) from err

    return Enumerable(record)


def _fetch_single(
    sqle: SQLEnumerableData,
    cursor: Cursor,
    cmd_to_execute: str,
) -> None | Enumerable:
    """
    Fetch cursor form a single request.

    Args:
        cmd_to_execute:Command which was executed.

    Returns:
        An Enumerable with the record or None if rowcount is not 1.

    Raises:
        CursorCloseError: If the cursor is already close. We proceed to a rollback.
        FetchError: If we have an error when fetching the cursor.
    """
    try:
        count = cursor.rowcount
    # For the moment I can't reproduce the error, but the test exists in:
    # tests/exceptions/test_execute.py.
    except InterfaceError as err:  # pragma: no cover
        if sqle.connection:
            sqle.connection.rollback()
        raise CursorCloseError(
            err,
            cmd_to_execute,
            "But the cursor is already closed. We proceed to a rollback",
            True,
        ) from err

    if count == 1:
        try:
            record = cursor.fetchall()
        # For the moment I can't reproduce the error, but the test exists in:
        # tests/exceptions/test_execute.py.
        except ProgrammingError as err:  # pragma: no cover
            cursor.close()
            if sqle.connection:
                sqle.connection.rollback()
            raise FetchError(
                err,
                cmd_to_execute,
                "But an error was caught in the data recovery. "
                "We proceed to a rollback rollback",
                True,
            ) from err
        return Enumerable(record)

    return None


def execute_select(  # noqa: C901
    cmd_to_execute: str,
    sqle: SQLEnumerableData,
) -> Enumerable | None:
    """
    Execute a selection command.

    Args:
        cmd_to_execute: The command to execute.
        sqle: SQLEnumerableData with information for execution.

    Returns:
        A tuple with the record if the query return a single element.
        A Enumerable with the record otherwise.

    Raises:
        CursorCloseError: If the cursor is already close. We proceed to a rollback or
            indirect raise by `_fetch_enumerable` or `_fetch_single.
        DatabError: If something wrong with the database.
        EmptyQueryError: If the query is empty.
        EmptyRecordError: If the record give by postgres is empty.
        FetchError: Indirect raise by `_fetch_enumerable` or `_fetch_single`.
    """
    # No coverage because is just another security but the exception was raised before.
    if not cmd_to_execute:
        # pylint: disable=duplicate-code
        raise EmptyQueryError(  # pragma: no cover
            ProgrammingError(),
            cmd_to_execute,
            "We can't execute empty request",
            False,
        ) from ProgrammingError
        # pylint enable=duplicate-code

    cursor = get_cursor(sqle.connection)

    query = sql.SQL(cmd_to_execute)

    try:
        cursor.execute(query)
    # No coverage because is just another security but the exception was raised before.
    except InvalidRowCountInResultOffsetClause as err:  # pragma: no cover
        if sqle.flags.default_cmd:
            sqle.connection.rollback()
            return None
        raise InvalidRowCountInResultOffsetClause from err
    except InvalidRowCountInLimitClause as err:  # pragma: no cover
        if sqle.flags.default_cmd:
            sqle.connection.rollback()
            return None
        raise InvalidRowCountInLimitClause from err
    # For the moment I can't reproduce the error, but the test exists in:
    # tests/exceptions/test_execute.py.
    except InterfaceError as err:  # pragma: no cover
        raise CursorCloseError(
            err,
            cmd_to_execute,
            "The cursor is already close",
            False,
        ) from err
    except DatabaseError as err:
        cursor.close()
        raise DatabError(
            err,
            cmd_to_execute,
            "Something wrong with database",
            False,
        ) from err

    if sqle.flags.terminal == Terminal.SINGLE:
        record = _fetch_single(sqle, cursor, cmd_to_execute)
    else:
        record = _fetch_enumerable(sqle, cursor, cmd_to_execute)

    if record is None and not sqle.flags.default_cmd:
        raise EmptyRecordError

    try:
        cursor.close()
    # For the moment I can't reproduce the error, but the test exists in:
    # tests/exceptions/test_execute.py.
    except InterfaceError as err:  # pragma: no cover
        if sqle.connection:
            sqle.connection.rollback()
        raise CursorCloseError(
            err,
            cmd_to_execute,
            "But the cursor is already close. We proceed to a rollback",
            True,
        ) from err

    logg.info("The command %s was executed.", cmd_to_execute)

    return record


def execute_alter(cmd_to_execute: str, sqle: SQLEnumerableData) -> int:
    """
    Execute a Alteration command.

    Args:
        cmd_to_execute: The command to execute.
        sqle: SQLEnumerableData with information for execution.

    Returns:
        A Number corresponding to the number of lines that will be affected.

    Raises:
        CursorCloseError: If the command is already close. We proceed to a rollback.
        EmptyQueryError: If the query is empty.
    """
    if not cmd_to_execute:
        # pylint: disable=duplicate-code
        # No coverage because is just another security,
        #  but the exception was raised before.
        raise EmptyQueryError(  # pragma: no cover
            ProgrammingError(),
            cmd_to_execute,
            "We can't execute empty request",
            False,
        ) from ProgrammingError
        # pylint: enable=duplicate-code

    cursor = get_cursor(sqle.connection)

    query = sql.SQL(cmd_to_execute)

    try:
        cursor.execute(query)
    # For the moment I can't reproduce the error, but the test exists in:
    # tests/exceptions/test_execute.py.
    except InterfaceError as err:  # pragma: no cover
        raise CursorCloseError(
            err,
            cmd_to_execute,
            "The cursor is already close",
            False,
        ) from err
    except DatabaseError as err:
        cursor.close()
        raise DatabError(
            err,
            cmd_to_execute,
            "Something wrong with database",
            False,
        ) from err

    record = cursor.rowcount

    try:
        cursor.close()
    # For the moment I can't reproduce the error, but the test exists in:
    # tests/exceptions/test_execute.py.
    except InterfaceError as err:  # pragma: no cover
        if sqle.connection:
            sqle.connection.rollback()
        raise CursorCloseError(
            err,
            cmd_to_execute,
            "But the cursor is already close. We proceed to a rollback",
            True,
        ) from err

    logg.info("The command %s was executed.", cmd_to_execute)

    return record


def execute_one(cmd_to_execute: str, sqle: SQLEnumerableData) -> bool:  # noqa: C901
    """
    Execute a command with a boolean record.

    Args:
        cmd_to_execute: The command to execute.
        sqle: SQLEnumerableData with information for execution.

    Returns:
        True if condition of the request is true,
        False otherwise.

    Raises:
        CursorCloseError: If the command is already close. We proceed to a rollback.
        EmptyQueryError: If the query is empty.
    """
    if not cmd_to_execute:
        # pylint: disable=duplicate-code
        # No coverage because is just another security,
        #  but the exception was raised before.
        raise EmptyQueryError(  # pragma: no cover
            ProgrammingError(),
            cmd_to_execute,
            "We can't execute empty request",
            False,
        ) from ProgrammingError
        # pylint: enable=duplicate-code

    cursor = get_cursor(sqle.connection)

    query = sql.SQL(cmd_to_execute)

    try:
        cursor.execute(query)
    # For the moment I can't reproduce the error, but the test exists in:
    # tests/exceptions/test_execute.py.
    except InterfaceError as err:  # pragma: no cover
        raise CursorCloseError(
            err,
            cmd_to_execute,
            "The cursor is already close",
            False,
        ) from err
    except DatabaseError as err:
        cursor.close()
        raise DatabError(
            err,
            cmd_to_execute,
            "Something wrong with database",
            False,
        ) from err

    record = cursor.fetchone()

    is_valid = False
    if cursor.rowcount >= 1 and sqle.cmd[0].cmd_type in [
        CommandType.ANY,
        CommandType.CONTAINS,
    ]:
        is_valid = True
    elif record and sqle.cmd[0].cmd_type == CommandType.ALL and record.case == 1:
        is_valid = True

    try:
        cursor.close()
    # For the moment I can't reproduce the error, but the test exists in:
    # tests/exceptions/test_execute.py.
    except InterfaceError as err:  # pragma: no cover
        if sqle.connection:
            sqle.connection.rollback()
        raise CursorCloseError(
            err,
            cmd_to_execute,
            "But the cursor is already closed. We proceed to a rollback",
            True,
        ) from err

    logg.info("The command %s was executed.", cmd_to_execute)

    if not record or not is_valid:
        return False

    return True
