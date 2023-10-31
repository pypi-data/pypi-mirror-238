"""Predicate functions used in py-linq-sql."""

# Standard imports
from typing import List

# Local imports
from ..classes.magicdotpath import BaseMagicDotPath, LambdaMagicDotPath, MagicDotPath
from ..classes.other_classes import SQLEnumerableData
from .path_functions import get_path


def get_one_predicate_as_str(
    sqle: SQLEnumerableData,
    mdpo: BaseMagicDotPath,
) -> str:
    """
    Get one predicate as string with the correct cast type and the correct prefix.

    Args:
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        mdpo: BasemagicDotPath to build the predicate.

    Returns:
        A predicate as a string with the correct cast type and prefix.

    Raises:
        psycopg.Error: Indirect raise by `get_path`.
        TableError: Indirect raise by `get_path`.
        TypeError: Indirect raise by `get_path`.
    """
    return get_path(mdpo, sqle)[0]


def get_predicates_as_str(
    result: List[str],
    fquery: LambdaMagicDotPath,
    sqle: SQLEnumerableData,
) -> None:
    """
    Get all predicates as string with the correct cast type and the correct prefix.

    Args:
        result: List contains the request.
        fquery: Lambda function to get paths.
        sqle: SQLEnumerableData with connection, flags, list of commands and a table.

    Returns:
        Predicates as a string with the correct cast type and prefix.

    Raises:
        TypeError: If the type of mdp_w_path isn't BaseMagicDotPath
            or tuple of BaseMagicDotPath,
            or indirect raise by `get_one_predicate_as_str`.
        psycopg.Error: Indirect raise by `get_one_predicate_as_str`.
        TableError: Indirect raise by `get_one_predicate_as_str`.
        TypeOperatorError: Indirect raise by `BaseMagicDotPath._get_number_operator`
            or `BaseMagicDotPath._get_generic_operator`.
    """
    mdp_w_path = fquery(MagicDotPath(sqle.connection))

    match mdp_w_path:
        case BaseMagicDotPath():
            result.append(get_one_predicate_as_str(sqle, mdp_w_path))
        case tuple():
            result.append(
                " AND ".join(
                    [get_one_predicate_as_str(sqle, mdp) for mdp in mdp_w_path],
                ),
            )
        case _:
            raise TypeError(
                "Only BaseMagicDotPath or tuple of BaseMagicDotPath are accepted.",
            )
