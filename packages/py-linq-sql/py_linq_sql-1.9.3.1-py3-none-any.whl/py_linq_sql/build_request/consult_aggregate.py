"""Functions for aggregation in group_by."""

# Local imports
from ..utils.classes.magicdotpath import (
    AggregateType,
    MagicDotPath,
    MagicDotPathAggregate,
)


def sum(  # noqa: A001
    mdp: MagicDotPath,
    cast_type: type = float,
) -> MagicDotPathAggregate:
    """
    Aggregate function to make a SUM.

    Args:
        mdp: A MagicDotPath to give the path of the function.
        cast_type: Type in which we want to cast the path(s). Its optional.
            By default: float

    Returns:
        MagicDotPathAggregate with the mdp and the type of aggregation.
    """
    return MagicDotPathAggregate(mdp, AggregateType.SUM, cast_type)


def avg(mdp: MagicDotPath, cast_type: type = float) -> MagicDotPathAggregate:
    """
    Aggregate function to make a AVG.

    Args:
        mdp: A MagicDotPath to give the path of the function.
        cast_type: Type in which we want to cast the path(s). Its optional.
            By default: float

    Returns:
        MagicDotPathAggregate with the mdp and the type of aggregation.
    """
    return MagicDotPathAggregate(mdp, AggregateType.AVG, cast_type)


def max(  # noqa: A001
    mdp: MagicDotPath,
    cast_type: type = float,
) -> MagicDotPathAggregate:
    """
    Aggregate function to make a MAX.

    Args:
        mdp: A MagicDotPath to give the path of the function.
        cast_type: Type in which we want to cast the path(s). Its optional.
            By default: float

    Returns:
        MagicDotPathAggregate with the mdp and the type of aggregation.
    """
    return MagicDotPathAggregate(mdp, AggregateType.MAX, cast_type)


def min(  # noqa: A001
    mdp: MagicDotPath,
    cast_type: type = float,
) -> MagicDotPathAggregate:
    """
    Aggregate function to make a MIN.

    Args:
        mdp: A MagicDotPath to give the path of the function.
        cast_type: Type in which we want to cast the path(s). Its optional.
            By default: float

    Returns:
        MagicDotPathAggregate with the mdp and the type of aggregation.
    """
    return MagicDotPathAggregate(mdp, AggregateType.MIN, cast_type)


def concat(
    mdp: MagicDotPath,
    separator: str,
) -> MagicDotPathAggregate:
    """
    Aggregate function to make a CONCAT.

    Args:
        mdp: A MagicDotPath to give the path of the function.

    Returns:
        MagicDotPathAggregate with the mdp, the type of aggregation and the separator.
    """
    return MagicDotPathAggregate(
        mdp,
        AggregateType.CONCAT,
        separator=separator,
        cast_type=str,
    )


def count(mdp: MagicDotPath, cast_type: type = float) -> MagicDotPathAggregate:
    """
    Aggregate function to make a COUNT.

    Args:
        - mdp: A MagicDotPath to give the path of the function.
        - cast_type: Type in which we want to cast the path(s). Its optional.
            By default: float

    Returns:
        MagicDotPathAggregate with the mdp and the type of aggregation.
    """
    return MagicDotPathAggregate(mdp, AggregateType.COUNT, cast_type)
