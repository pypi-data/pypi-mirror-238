"""All mathematics functions for MagicDotPath."""

# Standard imports
from decimal import Decimal

# Local imports
from ..classes.magicdotpath import BaseMagicDotPath, MagicDotPathWithOp
from ..classes.op_and_func_of_mdp import MathFunctType

_NUMBER_TYPE = float | int | Decimal


def cbrt(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Cube root function for a MagicDotPath.

    From psql docs: Cube root.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the cube root.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.CBRT,
    )


def sqrt(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Squart root function for a MagicDotPath.

    From psql docs: Square root.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the squart root.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.SQRT,
    )


def factorial(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Factorial function for a MagicDotPath.

    From psql docs: Factorial.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the factorial.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.FACTORIAL,
    )


def ceil(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Ceil function for a MagicDotPath.

    From psql docs: Nearest integer greater than or equal to argument.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the ceil.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.CEIL,
    )


def degrees(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Degrees function for a MagicDotPath.

    From psql docs: Converts radians to degrees.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the degrees.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.DEGREES,
    )


def floor(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Floor function for a MagicDotPath.

    From psql docs: Nearest integer less than or equal to argument.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the floor.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.FLOOR,
    )


def gcd(mdp: BaseMagicDotPath, other: _NUMBER_TYPE) -> MagicDotPathWithOp:
    """
    Gcd function for a MagicDotPath.

    From psql docs: Greatest common divisor (the largest positive number
    that divides both inputs with no remainder); returns 0 if both inputs are zero;
    available for integer, bigint, and numeric.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the gcd.
        other: An other element for the comparison.

    Returns:
        MagicDotPathWithOp with 2 operand and on the correct operator.

    Raises:
        TypeOperatorError: Indirect raise by `BaseMagicDotPath._get_number_operator`
    """
    return mdp._get_number_operator(  # pylint: disable=protected-access
        other,
        MathFunctType.GCD,
    )


def lcm(mdp: BaseMagicDotPath, other: _NUMBER_TYPE) -> MagicDotPathWithOp:
    """
    Lcm function for a MagicDotPath.

    From psql docs: Least common multiple (the smallest strictly positive number
    that is an integral multiple of both inputs); returns 0 if either input is zero;
    available for integer, bigint, and numeric.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the lcm.
        other: An other element for the comparison.

    Returns:
        MagicDotPathWithOp with 2 operand and on the correct operator.

    Raises:
        TypeOperatorError: Indirect raise by `BaseMagicDotPath._get_number_operator`
    """
    return mdp._get_number_operator(  # pylint: disable=protected-access
        other,
        MathFunctType.LCM,
    )


def exp(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Exp function for a MagicDotPath.

    From psql docs: Exponential (e raised to the given power).

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the exp.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.EXP,
    )


def ln(
    mdp: BaseMagicDotPath,
) -> MagicDotPathWithOp:
    """
    Ln function for a MagicDotPath.

    From psql docs: Natural logarithm.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the ln.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.LN,
    )


def log10(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Log10 function for a MagicDotPath.

    From psql docs: Base 10 logarithm.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the log10.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.LOG10,
    )


def log(mdp: BaseMagicDotPath, other: _NUMBER_TYPE) -> MagicDotPathWithOp:
    """
    Log function for a MagicDotPath.

    From psql docs: Logarithm of x to base b.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the log.
        other: Base for the logarithm.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.

    Raises:
        TypeOperatorError: Indirect raise by `BaseMagicDotPath._get_number_operator`
    """
    return mdp._get_number_operator(  # pylint: disable=protected-access
        other,
        MathFunctType.LOG,
    )


def min_scale(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Min scale function for a MagicDotPath.

    From psql docs: Minimum scale (number of fractional decimal digits) needed
    to represent the supplied value precisely.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the min scale.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.MIN_SCALE,
    )


def radians(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Radiant function for a MagicDotPath.

    From psql docs: Converts degrees to radians.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the radiant.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.RADIANS,
    )


def round(  # noqa: A001
    mdp: BaseMagicDotPath,
    other: _NUMBER_TYPE | None = None,
) -> MagicDotPathWithOp:
    """
    Round function for a MagicDotPath.

    From psql docs:

    - round(mdp): Rounds to nearest integer. For numeric,
        ties are broken by rounding away from zero.
        For double precision, the tie-breaking behavior is platform dependent,
        but “round to nearest even” is the most common rule.

    - round(mdp, other): Rounds v to s decimal places.
        Ties are broken by rounding away from zero.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the round.
        other: Number of decimal we want to keep.

    Returns:
        MagicDotPathWithOp with 2 operand and on the correct operator.

    Raises:
        TypeOperatorError: Indirect raise by `BaseMagicDotPath._get_number_operator`
    """
    if not other:
        other = 0

    return mdp._get_number_operator(  # pylint: disable=protected-access
        other,
        MathFunctType.ROUND,
    )


def scale(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Scale function for a MagicDotPath.

    From psql docs: Scale of the argument
    (the number of decimal digits in the fractional part).

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the scale.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.SCALE,
    )


def sign(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Sign function for a MagicDotPath.

    From psql docs: Sign of the argument (-1, 0, or +1).

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the sign.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.SIGN,
    )


def trim_scale(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Trim Scale function for a MagicDotPath.

    From psql docs: Reduces the value's scale (number of fractional decimal digits)
    by removing trailing zeroes.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the trim scale.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(  # pylint: disable=protected-access
        MathFunctType.TRIM_SCALE,
    )


def trunc(
    mdp: BaseMagicDotPath,
    other: _NUMBER_TYPE | None = None,
) -> MagicDotPathWithOp:
    """
    Trunc function for a MagicDotPath.

    From psql docs:

    - trunc(mdp): Truncates to integer (towards zero).

    - trunc(mdp, other): Truncates v to s decimal places.

    See: https://www.postgresql.org/docs/current/functions-math.html

    Args:
        mdp: MagicDotPath on which we apply the trunc.
        other: Number of decimal we want to keep.

    Returns:
        MagicDotPathWithOp with 2 operand and on the correct operator.

    Raises:
        TypeOperatorError: Indirect raise by `BaseMagicDotPath._get_number_operator`
    """
    if not other:
        other = 0

    return mdp._get_number_operator(  # pylint: disable=protected-access
        other,
        MathFunctType.TRUNC,
    )
