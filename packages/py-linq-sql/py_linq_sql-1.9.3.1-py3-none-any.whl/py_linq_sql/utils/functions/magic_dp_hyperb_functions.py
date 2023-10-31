"""All trigonometric functions for MagicDotPath."""

# Local imports
from ..classes.magicdotpath import BaseMagicDotPath, MagicDotPathWithOp
from ..classes.op_and_func_of_mdp import HyperBFuncType


def acosh(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Acosh function for a MagicDotPath.

    From psql docs: Inverse hyperbolic cosine.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the acosh.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        HyperBFuncType.ACOSH,
    )


def asinh(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Asinh function for a MagicDotPath.

    From psql docs: Inverse hyperbolic sine.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the asinh.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        HyperBFuncType.ASINH,
    )


def atanh(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Atanh function for a MagicDotPath.

    From psql docs: Inverse hyperbolic tangent.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the atanh.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        HyperBFuncType.ATANH,
    )


def cosh(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Cosh function for a MagicDotPath.

    From psql docs: Hyperbolic cosine.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the cosh.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        HyperBFuncType.COSH,
    )


def sinh(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Sinh function for a MagicDotPath.

    From psql docs: Hyperbolic sine.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the sinh.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        HyperBFuncType.SINH,
    )


def tanh(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Tanh function for a MagicDotPath.

    From psql docs: Hyperbolic tangent.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the tanh.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        HyperBFuncType.TANH,
    )
