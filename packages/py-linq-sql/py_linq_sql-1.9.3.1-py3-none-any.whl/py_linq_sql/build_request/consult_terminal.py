"""Build all terminal consult commands."""

# Local imports
from ..utils.classes.magicdotpath import MagicDotPath
from ..utils.classes.other_classes import Command, SQLEnumerableData
from ..utils.functions.aggregate_functions import get_aggregate
from ..utils.functions.other_functions import get_good_type
from ..utils.functions.path_functions import get_paths

# ---------------------
# |  Terminal builds  |
# ---------------------


def build_count() -> str:
    """
    Build a count request.

    Returns:
        Sub request to execute.
    """
    return "COUNT(*)"


def build_distinct() -> str:
    """
    Build a distinct request.

    Returns:
        Sub request to execute.
    """
    return "DISTINCT"


def build_except(command: Command) -> str:
    """
    Build an except request.

    Args:
        command: Command to build.

    Returns:
        Sub request to execute.
    """
    return f"EXCEPT {command.args.exclude_cmd}"


def build_group_by(
    command: Command,
    sqle: SQLEnumerableData,
) -> str:
    """
    Build a group_by request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.

    Returns:
        Sub request to execute.

    Raises:
        psycopg.Error: Indirect raise by `get_aggregate`.
        TableError: Indirect raise by `get_aggregate`.
        TypeError: Indirect raise by `get_aggregate`.
        TypeOperatorError: Indirect raise by `BaseMagicDotPath._get_number_operator`
            or `BaseMagicDotPath._get_generic_operator`.
    """
    aggreg_fquery = command.args.aggreg_fquery
    connection = sqle.connection

    mdp = MagicDotPath(connection)
    mdp_aggregate = aggreg_fquery(mdp)

    aggregate = get_aggregate(mdp_aggregate, sqle)

    return aggregate


def build_intersect(command: Command) -> str:
    """
    Build an intersect request.

    Args:
        command: Command to build.

    Returns:
        Sub request to execute.
    """
    built_sqle_2 = command.args.built_sqle_2

    result = ["INTERSECT"]

    result.append(built_sqle_2)

    return " ".join(result)


def build_max(command: Command, sqle: SQLEnumerableData) -> str:
    """
    Build a max request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.

    Returns:
        Sub request to execute.

    Raises:
        TypeError: If not get_good_type(cast_type) or indirect raise by `get_paths`.
        psycopg.Error: Indirect raise by `get_paths`.
        TableError: Indirect raise by `get_paths`.
        TypeOperatorError: Indirect raise by `get_paths`.
    """
    fquery = command.args.fquery
    cast_type = command.args.cast_type
    path = get_paths(fquery, sqle)[0]

    if not cast_type or cast_type == str:
        path = get_paths(fquery, sqle, True)[0]
        return f"MAX({path})"

    path = get_paths(fquery, sqle)[0]
    result = [f"MAX(CAST({path} AS"]

    casted_type = get_good_type(cast_type)

    if not casted_type:
        raise TypeError(f"Max take only int, float or date type, not {cast_type}")

    result.append(casted_type)

    return " ".join(result)


def build_min(command: Command, sqle: SQLEnumerableData) -> str:
    """
    Build a min request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.

    Returns:
        Sub request to execute.

    Raises:
        TypeError: If not get_good_type(cast_type) or indirect raise by `get_paths`.
        psycopg.Error: Indirect raise by `get_paths`.
        TableError: Indirect raise by `get_paths`.
        TypeOperatorError: Indirect raise by `get_paths`.
    """
    fquery = command.args.fquery
    cast_type = command.args.cast_type

    if not cast_type or cast_type == str:
        path = get_paths(fquery, sqle, True)[0]
        return f"MIN({path})"

    path = get_paths(fquery, sqle)[0]
    result = [f"MIN(CAST({path} AS"]

    casted_type = get_good_type(cast_type)

    if not casted_type:
        raise TypeError(f"Min take only int, float or date type, not {cast_type}")

    result.append(casted_type)

    return " ".join(result)


def build_union(command: Command) -> str:
    """
    Build an union request.

    Args:
        command: Command to build.

    Returns:
        Sub request to execute.
    """
    built_sqle_2 = command.args.built_sqle_2
    all_ = command.args.all_

    result = ["UNION ALL"] if all_ else ["UNION"]

    result.append(built_sqle_2)

    return " ".join(result)
