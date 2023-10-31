"""Aggregate functions used in py-linq-sql."""

# Standard imports
from typing import Tuple

# Local imports
from ..classes.magicdotpath import AggregateType, MagicDotPathAggregate
from ..classes.other_classes import SQLEnumerableData
from .other_functions import get_good_type
from .path_functions import get_path


def get_aggregate(
    mdpa: MagicDotPathAggregate | Tuple[MagicDotPathAggregate],
    sqle: SQLEnumerableData | None = None,
) -> str:
    """
    Get all built aggregate.

    Args:
        mdpa: MagicDotPathAggregate or tuple of MagicDotPathAggregate to build.
        sqle: SQLEnumerableData with connection, flags, list of commands and a table.

    Returns:
        All aggregate with paths as str.

    Raises:
        TypeError: If mdpa id not a MagicDotPathAggregate
            or indirect raise by `get_one_aggregate`.
        psycopg.Error: Indirect raise by `get_one_aggregate`.
        TableError: Indirect raise by `get_one_aggregate`.
    """
    result = []
    match mdpa:
        case MagicDotPathAggregate():
            result.append(get_one_aggregate(mdpa, mdpa.cast_type, sqle))
        case tuple():
            for idx, element in enumerate(mdpa):
                if not isinstance(element, MagicDotPathAggregate):
                    raise TypeError(
                        "get_aggregate_path take only MagicDotPathAggregate "
                        "or tuple of MagicDotPathAggregate.",
                    )
                result.append(get_one_aggregate(element, element.cast_type, sqle))

                if not idx == len(mdpa) - 1:
                    result.append(",")
        case _:
            raise TypeError(
                "get_aggregate_path take only MagicDotPathAggregate "
                "or tuple of MagicDotPathAggregate.",
            )

    return " ".join(result)


def get_one_aggregate(
    mdpa: MagicDotPathAggregate,
    cast_type: type,
    sqle: SQLEnumerableData | None,
) -> str:
    """
    Get one built aggregate.

    Args:
        mdpa: MagicDotPathAggregate to build.
        cast_type: Type in which we want to cast the path(s). Its optional.
        sqle: SQLEnumerableData with connection, flags, list of commands and a table.

    Returns:
        An aggregate with path as str.

    Raises:
        psycopg.Error: Indirect raise by `get_path` or `get_one_concat_aggregate`.
        TableError: Indirect raise by `get_path` or `get_one_concat_aggregate`.
        TypeError: Indirect raise by `get_path` or `get_one_concat_aggregate`.
    """
    if mdpa.operand == AggregateType.CONCAT:
        return get_one_concat_aggregate(mdpa, sqle)

    if cast_type == str:
        result = [f"{mdpa.operand}({get_path(mdpa.mdp, sqle)[0]})"]
    else:
        result = [f"{mdpa.operand}(CAST({get_path(mdpa.mdp, sqle)[0]} AS"]

        casted_type = get_good_type(cast_type)

        if not casted_type:
            raise TypeError(
                f"Group_by take only int, float, decimal or date type, not {cast_type}",
            )

        result.append(casted_type)

    return " ".join(result)


def get_one_concat_aggregate(
    mdpa: MagicDotPathAggregate,
    sqle: SQLEnumerableData | None,
) -> str:
    """
    Get one built concat aggregate.

    Args:
        mdpa: MagicDotPathAggregate to build.
        sqle: SQLEnumerableData with connection, flags, list of commands and a table.

    Returns:
        A concat aggregate with path as str.

    Raises:
        psycopg.Error: Indirect raise by `get_path`.
        TableError: Indirect raise by `get_path`.
        TypeError: Indirect raise by `get_path`.
    """
    return f"{mdpa.operand}({get_path(mdpa.mdp, sqle, True)[0]}, '{mdpa.separator}')"
