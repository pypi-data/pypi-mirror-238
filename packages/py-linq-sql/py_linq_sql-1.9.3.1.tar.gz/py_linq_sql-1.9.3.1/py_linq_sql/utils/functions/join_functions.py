"""Join functions used in py-linq-sql."""

# Standard imports
from typing import Callable, Dict, List, Tuple

# Third party imports
from dotmap import DotMap

# Local imports
from ..classes.enum import JoinType
from ..classes.magicdotpath import BaseMagicDotPath, LambdaMagicDotPath, MagicDotPath
from ..classes.other_classes import SQLEnumerableData
from .path_functions import get_path


def join_get_intersect(
    join_type: JoinType,
    outer_key_paths: List[str],
    inner_key_paths: List[str],
) -> str | None:
    """
    Get the correct WHERE subcommand depending on the type of join.

    Args:
        join_type: type of join.
        outer_key_paths: paths of the values to be compared of the outer SQLEnumerable.
        inner_key_paths: paths of the values to be compared og the inner SQLEnumerable.

    Return:
        A WHERE subcommand with the correct syntax for join or None
            if we make join with intersection.
    """
    result = []

    match join_type:
        case JoinType.LEFT_MINUS_INTERSECT | JoinType.RIGHT_MINUS_INTERSECT:
            result.append("WHERE")
            result.append(
                " AND ".join(
                    [f"{path_inner_k} IS NULL" for path_inner_k in inner_key_paths],
                ),
            )
            return " ".join(result)
        case JoinType.FULL_MINUS_INTERSECT:
            result.append("WHERE")
            result.append(
                " AND ".join(
                    [
                        f"{path_outer_k} IS NULL OR {path_inner_k} IS NULL"
                        for (path_outer_k, path_inner_k) in zip(
                            outer_key_paths,
                            inner_key_paths,
                        )
                    ],
                ),
            )
            return " ".join(result)
        case _:
            return None


def join_get_paths(
    outer: SQLEnumerableData,
    inner: SQLEnumerableData,
    inner_key: LambdaMagicDotPath,
    outer_key: LambdaMagicDotPath,
    result_function: Callable[
        [BaseMagicDotPath, BaseMagicDotPath],
        BaseMagicDotPath | Tuple[BaseMagicDotPath] | Dict[str, BaseMagicDotPath],
    ]
    | None,
) -> DotMap:
    """
    Get all paths for join.

    Args:
        outer: An other SQLEnumerable to make the join.
        inner: An SQLEnumerable to make the join.
        inner_key: lambda to select the value to be compared of the inner
            SQLEnumerable.
        outer_key: lambda to select the value to be compared of the outer
            SQLEnumerable.
        result_function: lambda the select the values to be returned.

    Returns:
        All paths we will used in the join.

    Raises:
        psycopg.Error: Indirect raise by `get_path`.
        TableError: Indirect raise by `get_path`.
        TypeError: Indirect raise by `get_path`.
    """
    obj_inner = MagicDotPath(inner.connection, with_table=inner.table)
    obj_outer = MagicDotPath(outer.connection, with_table=outer.table)

    paths = DotMap(
        select_paths=None,
        outer_key_paths=get_path(outer_key(obj_outer)),
        inner_key_paths=get_path(inner_key(obj_inner)),
    )

    if result_function:
        paths.select_paths = get_path(result_function(obj_inner, obj_outer))

    return paths
