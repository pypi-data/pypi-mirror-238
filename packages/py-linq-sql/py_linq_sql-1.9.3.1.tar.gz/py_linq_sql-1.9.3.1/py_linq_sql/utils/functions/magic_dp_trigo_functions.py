"""All trigonometric functions for MagicDotPath."""

# Standard imports
from decimal import Decimal

# Local imports
from ..classes.magicdotpath import BaseMagicDotPath, MagicDotPathWithOp
from ..classes.op_and_func_of_mdp import TrigoFunctType

_NUMBER_TYPE = float | int | Decimal


def acos(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Acos function for a MagicDotPath.

    From psql docs: Inverse cosine, result in radians.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the acos.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.ACOS,
    )


def acosd(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Acosd function for a MagicDotPath.

    From psql docs: Inverse cosine, result in degrees.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the acosd.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.ACOSD,
    )


def asin(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Asin function for a MagicDotPath.

    From psql docs: Inverse sine, result in radians.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the asin.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.ASIN,
    )


def asind(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Asind function for a MagicDotPath.

    From psql docs: Inverse sine, result in degrees.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the asind.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.ASIND,
    )


def atan(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Atan function for a MagicDotPath.

    From psql docs: Inverse tangent, result in radians.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the atan.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.ATAN,
    )


def atand(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Atand function for a MagicDotPath.

    From psql docs: Inverse tangent, result in degrees.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the atand.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.ATAND,
    )


def atan2(mdp: BaseMagicDotPath, other: _NUMBER_TYPE) -> MagicDotPathWithOp:
    """
    Atan2 function for a MagicDotPath.

    From psql docs: Inverse tangent of y/x, result in radians.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath representing x.
        other: number representing y.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.

    Raises:
        TypeOperatorError: Indirect raise by `BaseMagicDotPath._get_number_operator`
    """
    return mdp._get_number_operator(  # pylint: disable=protected-access
        other,
        TrigoFunctType.ATAN2,
    )


def atan2d(mdp: BaseMagicDotPath, other: _NUMBER_TYPE) -> MagicDotPathWithOp:
    """
    Atan2d function for a MagicDotPath.

    From psql docs: Inverse tangent of y/x, result in degrees.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath representing x.
        other: number representing y.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.

    Raises:
        TypeOperatorError: Indirect raise by `BaseMagicDotPath._get_number_operator`
    """
    return mdp._get_number_operator(  # pylint: disable=protected-access
        other,
        TrigoFunctType.ATAN2D,
    )


def cos(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Cos function for a MagicDotPath.

    From psql docs: Cosine, argument in radians.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the cos.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.COS,
    )


def cosd(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Cosd function for a MagicDotPath.

    From psql docs: Cosine, argument in degrees.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the cosd.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.COSD,
    )


def cot(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Cot function for a MagicDotPath.

    From psql docs: Cotangent, argument in radians.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the cot.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.COT,
    )


def cotd(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Cotd function for a MagicDotPath.

    From psql docs: Cotangent, argument in degrees.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the cotd.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.COTD,
    )


def sin(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Sin function for a MagicDotPath.

    From psql docs: Sine, argument in radians.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the sin.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.SIN,
    )


def sind(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Sind function for a MagicDotPath.

    From psql docs: Sine, argument in degrees.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the sind.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.SIND,
    )


def tan(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Tand function for a MagicDotPath.

    From psql docs: Tangent, argument in radians.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the tan.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.TAN,
    )


def tand(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Tand function for a MagicDotPath.

    From psql docs: Tangent, argument in degrees.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the tand.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        TrigoFunctType.TAND,
    )
