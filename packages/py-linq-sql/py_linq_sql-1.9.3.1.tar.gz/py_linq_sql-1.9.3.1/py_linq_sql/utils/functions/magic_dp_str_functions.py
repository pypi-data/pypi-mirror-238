"""All str functions for MagicDotPath."""

# Local imports
from ..classes.magicdotpath import BaseMagicDotPath, MagicDotPathWithOp
from ..classes.op_and_func_of_mdp import StrFunctType


def lower(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Lower function for a MagicDotPath.

    From psql docs: Converts the string to all lower case,
        according to the rules of the database's locale.

    See: https://www.postgresql.org/docs/14/functions-string.html

    Args:
        mdp: MagicDotPath on which we apply the lower.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(StrFunctType.LOWER)


def upper(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Upper function for a MagicDotPath.

    From psql docs: Converts the string to all upper case,
        according to the rules of the database's locale.

    See: https://www.postgresql.org/docs/14/functions-string.html

    Args:
        mdp: MagicDotPath on which we apply the upper.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(StrFunctType.UPPER)


def title(mdp: BaseMagicDotPath) -> MagicDotPathWithOp:
    """
    Title function for a MagicDotPath.

    From psql docs: Converts the first letter of each word to upper case and the rest
        to lower case. Words are sequences of alphanumeric characters separated by
        non-alphanumeric characters.

    See: https://www.postgresql.org/docs/14/functions-string.html

    Args:
        mdp: MagicDotPath on which we apply the title.

    Returns:
        MagicDotPathWithOp with one operand and on the correct operator.
    """
    return mdp._get_one_operand_operator(StrFunctType.INITCAP)
