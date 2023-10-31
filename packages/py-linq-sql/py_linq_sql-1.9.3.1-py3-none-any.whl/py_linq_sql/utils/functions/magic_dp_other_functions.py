"""All other functions for MagicDotPath."""

# Standard imports
from decimal import Decimal

# Local imports
from ..classes.magicdotpath import BaseMagicDotPath, MagicDotPathWithOp
from ..classes.op_and_func_of_mdp import OperatorType

_VALID_OPERAND_TYPE = float | int | str | list | dict | Decimal


def is_in(
    mdp: BaseMagicDotPath,
    other: list[_VALID_OPERAND_TYPE],
) -> MagicDotPathWithOp:
    """
    In function for a MagicDotPath.

    Know if a element is in a list of element.

    Args:
        mdp: MagicDotPath on which we want to known if is in a list.
        other: list of element.

    Returns:
        MagicDotPathWithOp with 2 operand and on the correct operator.

    Raises:
        TypeOperatorError: Indirect raised by _get_generic_operator.
    """
    return mdp._get_generic_operator(other, OperatorType.IN)
