"""Classes of MagicDotPath and specific enum, TypeAlias, functions for MDP."""

# Future imports
from __future__ import annotations

# Standard imports
import json
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from types import NoneType
from typing import Any, Callable, Dict, Tuple, Type, TypeAlias

# Third party imports
from dotmap import DotMap
from psycopg import Connection, sql

# Local imports
from ...exception.exception import TypeOperatorError
from .op_and_func_of_mdp import (
    HyperBFuncType,
    MathFunctType,
    OperatorType,
    StrFunctType,
    TrigoFunctType,
    col_name_hyper,
    col_name_math,
    col_name_ope,
    col_name_str,
    col_name_trigo,
    json_path_hyper,
    json_path_math,
    json_path_ope,
    json_path_str,
    json_path_trigo,
)

# In python 3.11, the enumerables have been changed,
# https://docs.python.org/3/whatsnew/3.11.html#enum, so that py-linq-sql is compatible
#  with versions 3.10 and 3.11 without having 2 different packages, we use the
# LowercaseStrEnums of strenum, https://pypi.org/project/StrEnum/, for versions lower
# than python 3.11 and the StrEnums of python 3.11 for versions greater than python 3.10
if sys.version_info >= (3, 11):
    # Standard imports
    from enum import StrEnum  # pragma: no cover
else:
    # Third party imports
    from strenum import LowercaseStrEnum as StrEnum  # pragma: no cover


_VALID_OPERAND_TYPE = float | int | str | list | dict | Decimal | bool
_OPERATORTYPE = (
    HyperBFuncType | MathFunctType | OperatorType | TrigoFunctType | StrFunctType
)
# ---------------
# |  Functions  |
# ---------------


def _clean_number_str(str_to_clean: str) -> str:
    """
    Clear a string representing a number (int or float).

    Replace all '.' by '_', '+' by 'plus' and '-' by 'minus'.

    Args:
        str_to_clean: string to reformat.

    Returns:
        The string at the good format.

    Examples:
        >>> _clean_number_str("2.0")
        '2_0'
        >>> _clean_number_str("-8")
        'minus8'
        >>> _clean_number_str("+12")
        'plus12'
        >>> _clean_number_str("-22.075")
        'minus22_075'
    """
    return str_to_clean.replace(".", "_").replace("+", "plus").replace("-", "minus")


# ----------
# |  Enum  |
# ----------


class AggregateType(StrEnum):
    """Enum of aggregation type."""

    SUM = "SUM"
    AVG = "AVG"
    MAX = "MAX"
    MIN = "MIN"
    COUNT = "COUNT"
    CONCAT = "STRING_AGG"


# -------------
# |  Classes  |
# -------------


class BaseMagicDotPath:
    """
    Abstract base for Magical object with operator methods.

    Inspired by The very useful [DotMap module](https://github.com/drgrib/dotmap) this
    object allow to write predicate in the lambda function used in SQL clause like
    `.select()` or `.join()`. This is very useful to express SQL constraint.

    See the LINQ documentation for more in depth explanation.

    """

    def __getattr__(self, attribute_name: str) -> BaseMagicDotPath:
        """
        Get attribute in a list for a MagicDotPath objects.

        Args:
            attribute_name: Names of all attributes.

        Returns:
            A MagicDotPath objects with attributes names in attributes list.

        Raises:
            NotImplementedError: This function is just a wrapper for the subclasses.
        """
        # No cover because is just a wrapper for subclasses.
        raise NotImplementedError  # pragma: no cover

    def __getitem__(self, attribute_name: str) -> BaseMagicDotPath:
        """
        Get items in a list for a MagicDotPath objects.

        Args:
            attribute_name: Names of all attributes.

        Returns:
            A MagicDotPath objects with attributes names in attributes list.

        Raises:
            NotImplementedError: This function is just a wrapper for the subclasses.
        """
        # No cover because is just a wrapper for subclasses.
        raise NotImplementedError  # pragma: no cover

    def _get_number_operator(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
        operator: _OPERATORTYPE,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a number operator.

        Args:
            other: Second objects for the comparison.
            operator: type of the operator.

        Returns:
            A MagicDotPathWithOp contains two operand and an operator
            with the correct type.

        Raises:
            TypeOperatorError: If the type of other is not accepted by the function.
            Accepted type: int, float, decimal, BaseMagicDotPath.
        """
        other_type: Type[Any]
        match other:
            case float():
                other_type = float
            case int():
                other_type = int
            case Decimal():
                other_type = Decimal
            case BaseMagicDotPath():
                other_type = BaseMagicDotPath
            case _:
                raise TypeOperatorError(
                    [int, float, Decimal, BaseMagicDotPath],
                    type(other),
                )
        return MagicDotPathWithOp(
            operand_1=self,
            operator=operator,
            operand_2=other,
            my_type=other_type,
        )

    def _get_generic_operator(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
        operator: _OPERATORTYPE,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a generic operator.

        Args:
            other: Second objects for the comparison.
            operator: type of the operator.

        Returns:
            A MagicDotPathWithOp contains two operand and an operator
            with the correct type.

        Raises:
            TypeOperatorError: If the type of other is not accepted by the function.
            Accepted type: int, float, decimal, str, list, dict, BaseMagicDotPath.
        """
        other_type: Type[Any] | None = None
        match other:
            case float():
                other_type = float
            case bool():
                other_type = bool
            case int():
                other_type = int
            case Decimal():
                other_type = Decimal
            case str():
                other_type = str
            case list():
                if operator == OperatorType.IN:
                    other_type = str
                else:
                    other_type = list
            case dict():
                other_type = dict
            case BaseMagicDotPath():
                other_type = BaseMagicDotPath
            case _:
                raise TypeOperatorError(
                    [float, int, Decimal, str, list, dict, bool, BaseMagicDotPath],
                    type(other),
                )
        return MagicDotPathWithOp(
            operand_1=self,
            operator=operator,
            operand_2=other,
            my_type=other_type,
        )

    def _get_one_operand_operator(self, operator: _OPERATORTYPE) -> MagicDotPathWithOp:
        """
        Get the operator for single operand MagicDotPathWithOp (~, abs, ...).

        Args:
            operator: The operator we want.

        Returns:
            A MagicDotPathWithOp contains an operand and an operator, operand_2 is None,
            with `~(x.data.obj.name) #not x.data.obj.name` we have only one operand and
            `my_type` is NoneType therefore.
        """
        return MagicDotPathWithOp(
            operand_1=self,
            operator=operator,
            operand_2=None,
            my_type=NoneType,
        )

    def __gt__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `>` operator and the correct types.

        Types are integer, float, Decimal or BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self._get_number_operator(other, OperatorType.GT)

    def __lt__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `<` operator and the correct types.

        Types are integer, float, Decimal or BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self._get_number_operator(other, OperatorType.LT)

    def __ge__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `>=` operator and the correct types.

        Types are integer, float, Decimal or BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self._get_number_operator(other, OperatorType.GE)

    def __le__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `<=` operator and the correct types.

        Types are integer, float, Decimal or BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self._get_number_operator(other, OperatorType.LE)

    def __eq__(  # type: ignore[override]
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `=` operator and the correct types.

        Types are integer, float, Decimal, string, list, dict, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_generic_operator`
        """
        return self._get_generic_operator(other, OperatorType.EQ)

    def __ne__(  # type: ignore[override]
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `<>` operator and the correct types.

        Types are integer, float, Decimal, string, list, dict, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_generic_operator`
        """
        return self._get_generic_operator(other, OperatorType.NE)

    def __add__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `+` operator and the correct types.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self._get_number_operator(other, OperatorType.ADD)

    def __radd__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `+` operator and the correct types.

        This operator is useful when we make `8 + MagicDotPath`
        and not `MagicDotPath + 8`.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self.__add__(other)

    def __sub__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `-` operator and the correct types.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self._get_number_operator(other, OperatorType.SUB)

    def __rsub__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `-` operator and the correct types.

        This operator is useful when we make `8 - MagicDotPath`
        and not `MagicDotPath - 8`.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        mdp_with_op = self._get_number_operator(self, OperatorType.SUB)
        mdp_with_op.operand_1 = other
        return mdp_with_op

    def __mul__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `*` operator and the correct types.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self._get_number_operator(other, OperatorType.MUL)

    def __rmul__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `*` operator and the correct types.

        This operator is useful when we make `8 * MagicDotPath`
        and not `MagicDotPath * 8`.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self.__mul__(other)

    def __truediv__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `/` operator and the correct types.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self._get_number_operator(other, OperatorType.TRUEDIV)

    def __rtruediv__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `/` operator and the correct types.

        This operator is useful when we make `8 / MagicDotPath`
        and not `MagicDotPath / 8`.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        mdp_with_op = self._get_number_operator(self, OperatorType.TRUEDIV)
        mdp_with_op.operand_1 = other
        return mdp_with_op

    def __mod__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `%` operator and the correct types.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self._get_number_operator(other, OperatorType.MOD)

    def __rmod__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `%` operator and the correct types.

        This operator is useful when we make `8 % MagicDotPath`
        and not `MagicDotPath % 8`.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        mdp_with_op = self._get_number_operator(self, OperatorType.MOD)
        mdp_with_op.operand_1 = other
        return mdp_with_op

    def __and__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `AND` operator and the correct types.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_generic_operator`
        """
        return self._get_generic_operator(other, OperatorType.AND)

    def __rand__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `AND` operator and the correct types.

        This operator is useful when we make `8 & MagicDotPath`
        and not `MagicDotPath & 8`.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_generic_operator`
        """
        return self.__and__(other)

    def __or__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `OR` operator and the correct types.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_generic_operator`
        """
        return self._get_generic_operator(other, OperatorType.OR)

    def __ror__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `OR` operator and the correct types.

        This operator is useful when we make `8 | MagicDotPath`
        and not `MagicDotPath | 8`.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_generic_operator`
        """
        return self.__or__(other)

    def __invert__(self) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `NOT` operator.

        Returns:
            MagicDotPathWithOp.
        """
        return self._get_one_operand_operator(OperatorType.INVERT)

    def __pow__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `^` operator.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        return self._get_number_operator(other, OperatorType.POW)

    def __rpow__(
        self,
        other: _VALID_OPERAND_TYPE | BaseMagicDotPath,
    ) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `^` operator and the correct types.

        This operator is useful when we make `8 ^ MagicDotPath`
        and not `MagicDotPath ^ 8`.

        Types are integer, float, Decimal, BaseMagicDotPath.

        Args:
            other: The value at which the comparison is made.

        Returns:
            MagicDotPathWithOp.

        Raises:
            TypeOperatorError: Indirect raise by `_get_number_operator`
        """
        mdp_with_op = self._get_number_operator(self, OperatorType.POW)
        mdp_with_op.operand_1 = other
        return mdp_with_op

    def __abs__(self) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `abs()` operator.

        Returns:
            MagicDotPathWithOp.
        """
        return self._get_one_operand_operator(OperatorType.ABS)

    def __pos__(self) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `+` operator.

        Returns:
            MagicDotPathWithOp.
        """
        return self._get_one_operand_operator(OperatorType.POS)

    def __neg__(self) -> MagicDotPathWithOp:
        """
        Get a MagicDotPathWithOp objects with a `-` operator.

        Returns:
            MagicDotPathWithOp.
        """
        return self._get_one_operand_operator(OperatorType.NEG)

    def jsonb_path(self, as_str: bool) -> str:
        """
        Get the corresponding jsonb path from a MagicDotPath.

        Args:
            as_str: Boolean to force the request with json in str.

        Returns:
            A path with the correct jsonb syntax.

        Raises:
            NotImplementedError: This function is just a wrapper for the subclasses.
        """
        # No cover because is just a wrapper for subclasses.
        raise NotImplementedError  # pragma: no cover

    def col_name(self) -> str:
        """
        Get the corresponding column name form a MagicDotPath.

        Returns:
            A column name with the correct format.

        Raises:
            NotImplementedError: This function is just a wrapper for the subclasses.
        """
        # No cover because is just a wrapper for subclasses.
        raise NotImplementedError  # pragma: no cover


# -----------------
# |  DataClasses  |
# -----------------


@dataclass(eq=False)
class MagicDotPath(BaseMagicDotPath):
    """
    Magical object that can have any attribute.

    Inspired by The very useful [DotMap module](https://github.com/drgrib/dotmap) this
    object allow to write predicate in the lambda function used in SQL clause like
    `.select()` or `.join()`. This is very useful to express SQL constraint.

    See the LINQ documentation for more in depth explanation.

    Attributes:
        connection: Connection to a db. Useful for safe.
        attributes: Attributes for build the jsonb path.
        with_table: Table on which we want to get paths.
        column: Column on which we will want to make the request.

    """

    connection: Connection
    attributes: list[str] = field(default_factory=list)
    with_table: str | None = None
    column: str | None = None

    def __getattr__(self, attribute_name: str) -> MagicDotPath:
        """
        Get attribute in a list for a MagicDotPath objects.

        Args:
            attribute_name: Names of all attributes.

        Returns:
            A MagicDotPath objects with attributes names in attributes list.
        """
        return MagicDotPath(
            self.connection,
            attributes=self.attributes + [f"'{attribute_name}'"],
            with_table=self.with_table,
        )

    def __getitem__(self, attribute_name: str) -> MagicDotPath:
        """
        Get attr from the dict syntax.

        Args:
            attribute_name: Names of all attributes.

        Returns:
            A MagicDotPath objects with attributes names in attributes list.
        """
        return self.__getattr__(attribute_name)

    def safe(self, name: str) -> str:
        """
        Secure a column or a table for a request.

        Args:
            name: Name of the column or table we want to secure.

        Returns:
            Name but verified by psycopg.sql.Identifier.

        Raises:
            psycopg.Error: Indirect raise by `sql.Identifier` or `as_string`.
        """
        return sql.Identifier(name).as_string(self.connection)

    def format_table_with_dot(self) -> str:
        """
        Get the table with dot in good format.

        Returns:
            The table in the good psql format.
        """
        return ".".join(
            [f"{tab}" for tab in self.with_table.split(".")]  # type: ignore[union-attr]
        )

    def jsonb_path(self, as_str: bool) -> str:
        """
        Get the corresponding jsonb path from a MagicDotPath.

        Args:
            as_str: Boolean to force the request with json in str.

        Returns:
            A path with the correct jsonb syntax.

        Raises:
            psycopg.Error: Indirect raise by `safe`.
        """
        self.column = self.safe(self.attributes[0][1:-1])

        res = ""

        if self.with_table:
            table = (
                self.format_table_with_dot()
                if "." in self.with_table
                else f"{self.with_table}"
            )
            res = f"{res}{table}."

        if len(self.attributes) == 1:
            res = f"{res}{self.column}"
        else:
            if as_str:
                path_item = self.attributes[1:-1].copy()
                path_item.insert(0, self.column)
                res = f'{res}{"->".join(path_item)}->>{self.attributes[-1]}'
            else:
                res = f'{res}{self.column}->{"->".join(self.attributes[1:])}'
        return res

    def col_name(self) -> str:
        """
        Get the corresponding column name form a MagicDotPath.

        Returns:
            A column name with the correct format.
        """
        result = []

        if self.with_table:
            table = (
                self.format_table_with_dot()
                if "." in self.with_table
                else self.with_table
            )
            result.append(table[1:-1])

        for att in self.attributes:
            result.append(att[1:-1])

        return "_".join(result)


@dataclass(eq=False)
class MagicDotPathWithOp(BaseMagicDotPath):
    """
    Magical object that can have any attribute and can be subject to many comparison.

    This class inherited from MagicDotPath.

    Inspired by The very useful [DotMap module](https://github.com/drgrib/dotmap) this
    object allow to write predicate in the lambda function used in SQL clause like
    `.select()` or `.join()`. This is very useful to express SQL constraint.

    See the LINQ documentation for more in depth explanation.

    Attributes:
        operand_1: First operand for the operation.
        operand_2: Second operand for the operation.
        operator: Operator for comparison.
        my_type: Type of other.

    """

    operand_1: BaseMagicDotPath | _VALID_OPERAND_TYPE
    operator: _OPERATORTYPE
    operand_2: BaseMagicDotPath | _VALID_OPERAND_TYPE | None
    my_type: Type[Any]

    def jsonb_path(self, as_str: bool) -> str:
        """
        Get the corresponding jsonb path from a MagicDotPathWithOp.

        Args:
            as_str: Boolean to force the request with json in str.

        Returns:
            A path with the correct jsonb syntax.

        Raises:
            psycopg.Error: Indirect raise by `MagicDotPath.safe`.
            TypeOperatorError: Indirect raise by `json_path_hyper`, `json_path_math`,
                `json_path_ope` or `json_path_trigo`.
        """
        as_str = self.my_type == str

        path_op = DotMap()

        match self.operand_1:
            case MagicDotPath() | MagicDotPathWithOp():
                path_op.op1 = self.operand_1.jsonb_path(as_str)
            case _:
                path_op.op1 = str(self.operand_1)

        match self.operand_2:
            case MagicDotPath() | MagicDotPathWithOp():
                path_op.op2 = self.operand_2.jsonb_path(as_str)
            case dict():
                operand_2_in_good_format = json.dumps(self.operand_2)
                path_op.op2 = f"'{operand_2_in_good_format}'::jsonb"
            case list():
                if self.operator in [OperatorType.IN]:
                    path_op.op2 = (
                        f"""({", ".join([f"'{val}'" for val in self.operand_2])})"""
                    )
                else:
                    path_op.op2 = f"'{self.operand_2}'::jsonb"
            case _:
                path_op.op2 = str(self.operand_2)

        match self.my_type:
            case type() if self.my_type == bool:
                result = (
                    f"CAST({path_op.op1} AS boolean) {self.operator.psql} {path_op.op2}"
                )
            case type() if self.operator in [
                OperatorType.AND,
                OperatorType.OR,
                OperatorType.INVERT,
                OperatorType.ABS,
                OperatorType.POS,
                OperatorType.NEG,
                OperatorType.IN,
            ]:
                result = json_path_ope(path_op, self.operator)
            case type() if isinstance(self.operator, HyperBFuncType):
                result = json_path_hyper(path_op, self.operator)
            case type() if isinstance(self.operator, MathFunctType):
                result = json_path_math(path_op, self.operator)
            case type() if isinstance(self.operator, TrigoFunctType):
                result = json_path_trigo(path_op, self.operator)
            case type() if isinstance(self.operator, StrFunctType):
                result = json_path_str(path_op, self.operator)
            case type() if self.my_type == BaseMagicDotPath:
                result = (
                    f"CAST({path_op.op1} AS decimal) "
                    f"{self.operator.psql} "
                    f"CAST({path_op.op2} AS decimal)"
                )
            case type() if self.my_type in (int, float, Decimal):
                result = (
                    f"CAST({path_op.op1} AS decimal) {self.operator.psql} {path_op.op2}"
                )
            case type() if self.my_type == str:
                result = f"{path_op.op1} {self.operator.psql} '{path_op.op2}'"
            case _:
                result = f"{path_op.op1} {self.operator.psql} {path_op.op2}"

        return result

    def col_name(self) -> str:
        """
        Get the corresponding column name form a MagicDotPath.

        Returns:
            A column name with the correct format.

        Raises:
            TypeOperatorError: Indirect raise by `col_name_hyper`, `col_name_math`,
                `col_name_ope` or `col_name_trigo`.
        """
        name_op = DotMap()

        match self.operand_1:
            case BaseMagicDotPath():
                name_op.op1 = self.operand_1.col_name()
            case _:
                name_op.op1 = str(self.operand_1)

        match self.operand_2:
            case None:
                name_op.op2 = None
            case BaseMagicDotPath():
                name_op.op2 = self.operand_2.col_name()
            case float() | int() | Decimal():
                name_op.op2 = _clean_number_str(str(self.operand_2))
            # TODO: test this
            case list():
                name_op.op2 = f"""({','.join([str(val) for val in self.operand_2])})"""

        operator = self.operator
        match operator:
            case operator if operator in HyperBFuncType:
                result = col_name_hyper(name_op, operator)
            case operator if operator in MathFunctType:
                result = col_name_math(name_op, operator)
            case operator if operator in OperatorType:
                result = col_name_ope(name_op, operator)
            case operator if operator in TrigoFunctType:
                result = col_name_trigo(name_op, operator)
            case operator if operator in StrFunctType:
                result = col_name_str(name_op, operator)
            # No cover because is just an other security,
            # but we can't go in this case thanks to Enum.
            case _:  # pragma: no cover
                result = f"{name_op.op1}_???_{name_op.op2}"

        return f"{result}"


@dataclass
class MagicDotPathAggregate:
    """
    MagicDotPath for aggregation.

    Attributes:
        mdp: A MagicDotPath.
        operand: Aggregation type.
        separator: Separator for string_agg aggregate. In other case its None.

    """

    mdp: MagicDotPath
    operand: AggregateType | str  # HACK: It's just the time that mypy supports the
    # Strenum. https://github.com/python/mypy/issues
    cast_type: type
    separator: str | None = None


# ------------------
# |  Type Aliases  |
# ------------------

# Type for the lambda in SQLEnuemrable methods who take a MagicDotPath and return:
# MagicDotPath
# or Tuple of MagicDotPath
# or Dict of MagicDotPath
LambdaMagicDotPath: TypeAlias = Callable[
    [BaseMagicDotPath],
    BaseMagicDotPath | Tuple[BaseMagicDotPath] | Dict[str, BaseMagicDotPath],
]

LambdaMagicDotPathAggregate: TypeAlias = Callable[
    [MagicDotPath | MagicDotPathAggregate],
    MagicDotPath
    | MagicDotPathAggregate
    | Tuple[MagicDotPath | MagicDotPathAggregate]
    | Dict[str, MagicDotPath | MagicDotPathAggregate],
]
