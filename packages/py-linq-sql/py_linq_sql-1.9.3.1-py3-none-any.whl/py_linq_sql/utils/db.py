"""File to manage the data base, connect, get a cursor on this connection."""

# Third party imports
import psycopg
from psycopg import Connection, Cursor, Error

# Local imports
from ..exception.exception import PSQLConnectionError


def connect(
    user: str,
    password: str,
    host: str,
    port: str,
    database: str,
) -> Connection:
    """
    Connect to a database.

    Args:
        user: User used to log in to the database.
        password: Password of the user.
        host: Host used for the connection.
        port: Port used for the connection.
        database: Database to which we want to connect.

    Returns:
        A connection to a database if all is working.

    Raises:
        PSQLConnectionError: If we have an error connecting to the database.
    """
    try:  # pragma: no cover
        connection = psycopg.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            dbname=database,
        )
        return connection
    except (Exception, Error) as err:  # pragma: no cover
        raise PSQLConnectionError(f"Error while connecting to posgeSQL {err}") from err


def get_cursor(connection: Connection) -> Cursor:
    """
    Get a cursor on the given connection.

    Args:
        connection: A connection to a database on which we want to execute commands.

    Returns:
        A cursor on the given connection to a data base to execute commands.
    """
    cursor = connection.cursor(row_factory=psycopg.rows.namedtuple_row)
    return cursor
