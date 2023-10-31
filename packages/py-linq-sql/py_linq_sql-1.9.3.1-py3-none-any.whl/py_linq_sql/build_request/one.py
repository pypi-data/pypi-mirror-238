"""Build all One commands."""

# Standard imports
from typing import Any, Dict

# Local imports
from ..utils.classes.other_classes import Command, SQLEnumerableData
from ..utils.functions.other_functions import get_json
from ..utils.functions.predicate_functions import get_predicates_as_str


def build_any(command: Command, sqle: SQLEnumerableData) -> str:
    """
    Build an any request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.

    Returns:
        Request to execute.

    Raises:
        psycopg.Error: Indirect raise by `get_predicates_as_str`.
        TableError: Indirect raise by `get_predicates_as_str`.
        TypeError: Indirect raise by `get_predicates_as_str`.
        TypeOperatorError: Indirect raise by `get_predicates_as_str`.
    """
    fquery = command.args.fquery

    result = [f"SELECT * FROM {sqle.table}"]

    if not fquery:
        return result[0]

    result.append("WHERE")

    get_predicates_as_str(result, fquery, sqle)

    return " ".join(result)


def build_all(command: Command, sqle: SQLEnumerableData) -> str:
    """
    Build an all request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.

    Returns:
        Request to execute.

    Raises:
        psycopg.Error: Indirect raise by `get_predicates_as_str`.
        TableError: Indirect raise by `get_predicates_as_str`.
        TypeError: Indirect raise by `get_predicates_as_str`.
        TypeOperatorError: Indirect raise by `get_predicates_as_str`.
    """
    fquery = command.args.fquery

    result = [f"SELECT CASE WHEN ((SELECT COUNT(*) FROM {sqle.table} WHERE"]

    get_predicates_as_str(result, fquery, sqle)

    result.append(
        f") = (SELECT COUNT(*) FROM {sqle.table})) THEN 1 ELSE 0 END FROM {sqle.table}",
    )

    return " ".join(result)


def _contains_dict(sqle: SQLEnumerableData, fquery: Dict[str, Any]) -> str:
    """
    Build the request for a contains on a dictionary.

    Args:
        fquery: dictionary which we want to know if it is in the database.

    Returns:
        The query built.

    Raises:
        ValueError: Indirect raise by `get_json`.
    """
    result = [f"SELECT * FROM {sqle.table} WHERE"]

    for idx, key in enumerate(fquery):
        if isinstance(fquery[key], dict):
            r_equal = f"'{get_json(fquery[key])}'"
        else:
            r_equal = fquery[key]

        result.append(f"{key} = {r_equal}")

        if not idx == len(fquery) - 1:
            result.append("AND")

    return " ".join(result)


def build_contains(command: Command, sqle: SQLEnumerableData) -> str:
    """
    Build an contains request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.

    Returns:
        Request to execute.

    Raises:
        psycopg.Error: Indirect raise by `build_any`.
        TableError: Indirect raise by `build_any`.
        TypeError: Indirect raise by `build_any`.
        TypeOperatorError: Indirect raise by `build_any`.
        ValueError: Indirect raise by `_contains_dict`.
    """
    fquery = command.args.fquery

    match fquery:
        case dict():
            return _contains_dict(sqle, fquery)
        case _:
            return build_any(command, sqle)
