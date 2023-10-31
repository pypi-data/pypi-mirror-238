"""OperatorsType, functionsType aand the functions that use them."""

# Standard imports
from collections import namedtuple
from enum import Enum

# Third party imports
from dotmap import DotMap

# Local imports
from ...exception.exception import TypeOperatorError

# We separate the different operators and functions for more readability.

# -----------------
# |  NamedTuples  |
# -----------------

_HyperBFunction = namedtuple("_HyperBFunction", ["python", "psql", "name"])
_MathFunction = namedtuple("_MathFunction", ["python", "psql", "name"])
_Operator = namedtuple("_Operator", ["python", "psql", "name"])
_TrigoFunction = namedtuple("_TrigoFunction", ["python", "psql", "name"])
_StrFunction = namedtuple("_StrFunction", ["python", "psql", "name"])

# ----------
# |  Enum  |
# ----------


class StrFunctType(_StrFunction, Enum):
    """Enum of string function type."""

    LOWER = _StrFunction(python="lower", psql="lower", name="lower")
    UPPER = _StrFunction(python="upper", psql="upper", name="upper")
    INITCAP = _StrFunction(python="title", psql="initcap", name="title")


class HyperBFuncType(_HyperBFunction, Enum):
    """Enum of hyperbolic function type."""

    ACOSH = _HyperBFunction(python="acosh", psql="acosh", name="acosh")
    ASINH = _HyperBFunction(python="asinh", psql="asinh", name="asinh")
    ATANH = _HyperBFunction(python="atanh", psql="atanh", name="atanh")
    COSH = _HyperBFunction(python="cosh", psql="cosh", name="cosh")
    SINH = _HyperBFunction(python="sinh", psql="sinh", name="sinh")
    TANH = _HyperBFunction(python="tanh", psql="tanh", name="tanh")


class MathFunctType(_MathFunction, Enum):
    """Enum of mathematical function type."""

    CBRT = _MathFunction(python="cbrt", psql="||/", name="cbrt")
    CEIL = _MathFunction(python="ceil", psql="ceil", name="ceil")
    DEGREES = _MathFunction(python="degrees", psql="degrees", name="degrees")
    EXP = _MathFunction(python="exp", psql="exp", name="exp")
    FACTORIAL = _MathFunction(python="factorial", psql="factorial", name="factorial")
    FLOOR = _MathFunction(python="floor", psql="floor", name="floor")
    GCD = _MathFunction(python="gcd ", psql="gcd", name="gcd")
    LCM = _MathFunction(python="lcm ", psql="lcm", name="lcm")
    LN = _MathFunction(python="log", psql="ln", name="ln")
    LOG = _MathFunction(python="log ", psql="log", name="log")
    LOG10 = _MathFunction(python="log10", psql="log10", name="log10")
    MIN_SCALE = _MathFunction(python=None, psql="min_scale", name="minScale")
    RADIANS = _MathFunction(python="radians ", psql="radians", name="radians")
    ROUND = _MathFunction(python="round", psql="round", name="round")
    SCALE = _MathFunction(python=None, psql="scale", name="scale")
    SIGN = _MathFunction(python="sign", psql="sign", name="sign")
    SQRT = _MathFunction(python="sqrt", psql="|/", name="sqrt")
    TRIM_SCALE = _MathFunction(python=None, psql="trim_scale", name="trimScale")
    TRUNC = _MathFunction(python="trunc", psql="trunc", name="trunc")


class OperatorType(_Operator, Enum):
    """Enum of operator type."""

    ABS = _Operator(python="abs", psql="@", name="abs")
    ADD = _Operator(python="+", psql="+", name="add")
    AND = _Operator(python="&", psql="AND", name="and")
    EQ = _Operator(python="==", psql="=", name="equal")
    GE = _Operator(python=">=", psql=">=", name="greater_equal")
    GT = _Operator(python=">", psql=">", name="greater")
    INVERT = _Operator(python="~", psql="NOT", name="not")
    LE = _Operator(python="<=", psql="<=", name="lesser_equal")
    LT = _Operator(python="<", psql="<", name="lesser")
    MOD = _Operator(python="%", psql="%", name="mod")
    MUL = _Operator(python="*", psql="*", name="mul")
    NE = _Operator(python="!=", psql="<>", name="not_equal")
    NEG = _Operator(python="-", psql="-", name="neg")
    OR = _Operator(python="|", psql="OR", name="or")
    POS = _Operator(python="+", psql="+", name="pos")
    POW = _Operator(python="**", psql="^", name="pow")
    SUB = _Operator(python="-", psql="-", name="sub")
    TRUEDIV = _Operator(python="/", psql="/", name="div")
    IN = _Operator(python="in", psql="IN", name="in")


class TrigoFunctType(_TrigoFunction, Enum):
    """Enum of trigonometric function type."""

    ACOS = _TrigoFunction(python="acos", psql="acos", name="acos")
    ACOSD = _TrigoFunction(python=None, psql="acosd", name="acosd")
    ASIN = _TrigoFunction(python="asin", psql="asin", name="asin")
    ASIND = _TrigoFunction(python=None, psql="asind", name="asind")
    ATAN = _TrigoFunction(python="atan", psql="atan", name="atan")
    ATAND = _TrigoFunction(python=None, psql="atand", name="atand")
    ATAN2 = _TrigoFunction(python="atan2", psql="atan2", name="atan2")
    ATAN2D = _TrigoFunction(python=None, psql="atan2d", name="atan2d")
    COS = _TrigoFunction(python="cos", psql="cos", name="cos")
    COSD = _TrigoFunction(python=None, psql="cosd", name="cosd")
    COT = _TrigoFunction(python="cot", psql="cot", name="cot")
    COTD = _TrigoFunction(python=None, psql="cotd", name="cotd")
    SIN = _TrigoFunction(python="sin", psql="sin", name="sin")
    SIND = _TrigoFunction(python=None, psql="sind", name="sind")
    TAN = _TrigoFunction(python="tan", psql="tan", name="tan")
    TAND = _TrigoFunction(python=None, psql="tand", name="tand")


# ---------------
# |  Functions  |
# ---------------

_OPERATORTYPE = (
    HyperBFuncType | MathFunctType | OperatorType | TrigoFunctType | StrFunctType
)


def col_name_hyper(name_op: DotMap, operator: _OPERATORTYPE) -> str:
    """
    Get the corresponding column name for an hyperbolic functions from a MagicDotPath.

    Args:
        name_op: name of the operand(s).
        operator: Operator Type.

    Returns:
        A column name with the correct format.

    Raises:
        TypeOperatorError: If type of operator is not `HyperBFuncType`.

    Examples:
        >>> col_name_hyper(DotMap(op1="mass"), HyperBFuncType.COSH)
        'cosh_mass'
    """
    if not isinstance(operator, HyperBFuncType):
        raise TypeOperatorError([HyperBFuncType], type(operator))

    return f"{operator.name}_{name_op.op1}"


def col_name_math(name_op: DotMap, operator: _OPERATORTYPE) -> str:
    """
    Get the corresponding column name for a mathematical functions from a MagicDotPath.

    Args:
        name_op: name of the operand(s).
        operator: Operator Type.

    Returns:
        A column name with the correct format.

    Raises:
        TypeOperatorError: If type of operator is not `MathFunctType`.

    Examples:
        >>> col_name_math(DotMap(op1="mass"), MathFunctType.CEIL)
        'ceil_mass'
    """
    if not isinstance(operator, MathFunctType):
        raise TypeOperatorError([MathFunctType], type(operator))

    if operator in [
        MathFunctType.GCD,
        MathFunctType.LCM,
        MathFunctType.LOG,
        MathFunctType.ROUND,
        MathFunctType.TRUNC,
    ]:
        return f"{operator.name}_{name_op.op1}_{name_op.op2}"

    return f"{operator.name}_{name_op.op1}"


def col_name_ope(name_op: DotMap, operator: _OPERATORTYPE) -> str:
    """
    Get the corresponding column name for an operator from a MagicDotPath.

    Args:
        name_op: name of the operand(s).
        operator: Operator Type.

    Returns:
        A column name with the correct format.

    Raises:
        TypeOperatorError: If type of operator is not `OperatorType.`.

    Examples:
        >>> col_name_ope(DotMap(op1="mass", op2="power"), OperatorType.POW)
        'mass_pow_power'
    """
    if not isinstance(operator, OperatorType):
        raise TypeOperatorError([OperatorType], type(operator))

    if operator in [
        OperatorType.ABS,
        OperatorType.NEG,
        OperatorType.POS,
        OperatorType.INVERT,
    ]:
        return f"{operator.name}_{name_op.op1}"

    return f"{name_op.op1}_{operator.name}_{name_op.op2}"


def col_name_trigo(name_op: DotMap, operator: _OPERATORTYPE) -> str:
    """
    Get the corresponding column name for a trigonometric functions from a MagicDotPath.

    Args:
        name_op: name of the operand(s).
        operator: Operator Type.

    Returns:
        A column name with the correct format.

    Raises:
        TypeOperatorError: If type of operator is not `TrigoFunctType`.

    Examples:
        >>> col_name_trigo(DotMap(op1="mass"), TrigoFunctType.ASIND)
        >>> "asind_mass"
    """
    if not isinstance(operator, TrigoFunctType):
        raise TypeOperatorError([TrigoFunctType], type(operator))

    if operator in [TrigoFunctType.ATAN2, TrigoFunctType.ATAN2D]:
        return f"{operator.name}_{name_op.op1}_{name_op.op2}"

    return f"{operator.name}_{name_op.op1}"


def col_name_str(name_op: DotMap, operator: _OPERATORTYPE) -> str:
    """
    Get the corresponding column name for a str functions from a MagicDotPath.

    Args:
        name_op: name of the operand(s).
        operator: Operator Type.

    Returns:
        A column name with correct format.

    Raises:
        TypeOperatorErrir: If type of operator is not `StrFunctType`.

    Examples:
        >>> col_name_str(DotMap(op1="star_name"), StrFunctType.LOWER)
        >>> 'lower_star_name'
    """
    if not isinstance(operator, StrFunctType):
        raise TypeOperatorError([StrFunctType], type(operator))

    return f"{operator.name}_{name_op.op1}"


def json_path_hyper(path_op: DotMap, operator: _OPERATORTYPE) -> str:
    """
    Get the corresponding jsonb path for an hyperbolic function from a MagicDotPath.

    Args:
        path_op: path of the operand(s).
        operator: Operator Type.

    Returns:
        A path with the correct jsonb syntax.

    Raises:
        TypeOperatorError: If type of operator is not `HyperBFuncType`.
    """
    if not isinstance(operator, HyperBFuncType):
        raise TypeOperatorError([HyperBFuncType], type(operator))

    return f"{operator.psql}(CAST({path_op.op1} AS decimal))"


def json_path_math(path_op: DotMap, operator: _OPERATORTYPE) -> str:
    """
    Get the corresponding jsonb path for a mathematical function from a MagicDotPath.

    Args:
        path_op: path of the operand(s).
        operator: Operator Type.

    Returns:
        A path with the correct jsonb syntax.

    Raises:
        TypeOperatorError: If type of operator is not `MathFunctType`.
    """
    if not isinstance(operator, MathFunctType):
        raise TypeOperatorError([MathFunctType], type(operator))

    if operator in [MathFunctType.FACTORIAL]:
        return f"{operator.psql}(CAST({path_op.op1} AS integer))"

    if operator in [
        MathFunctType.SQRT,
        MathFunctType.CBRT,
    ]:
        return f"{operator.psql} CAST({path_op.op1} AS decimal)"

    if operator in [MathFunctType.GCD, MathFunctType.LCM]:
        operand_1 = f"CAST({path_op.op1} AS integer)"
        operand_2 = f"CAST({path_op.op2} AS integer)"
        return f"{operator.psql}({operand_1}, {operand_2})"

    if operator in [MathFunctType.TRUNC, MathFunctType.ROUND]:
        return f"{operator.psql}(CAST({path_op.op1} AS decimal), {path_op.op2})"

    if operator in [MathFunctType.LOG]:
        return f"{operator.psql}({path_op.op2}, CAST({path_op.op1} AS decimal))"

    return f"{operator.psql}(CAST({path_op.op1} AS decimal))"


def json_path_ope(path_op: DotMap, operator: _OPERATORTYPE) -> str:
    """
    Get the corresponding jsonb path for an operator from a MagicDotPath.

    Args:
        path_op: path of the operand(s).
        operator: Operator Type.

    Returns:
        A path with the correct jsonb syntax.

    Raises:
        TypeOperatorError: If type of operator is not `OperatorType`.
    """
    if not isinstance(operator, OperatorType):
        raise TypeOperatorError([OperatorType], type(operator))

    if operator in [OperatorType.AND, OperatorType.OR, OperatorType.IN]:
        return f"{path_op.op1} {operator.psql} {path_op.op2}"

    if operator in [OperatorType.INVERT]:
        return f"{operator.psql} {path_op.op1}"

    return f"{operator.psql} CAST({path_op.op1} AS decimal)"


def json_path_trigo(path_op: DotMap, operator: _OPERATORTYPE) -> str:
    """
    Get the corresponding jsonb path for a trigonometric function from a MagicDotPath.

    Args:
        path_op: path of the operand(s).
        operator: Operator Type.

    Returns:
        A path with the correct jsonb syntax.

    Raises:
        TypeOperatorError: If type of operator is not `TrigoFunctType`.
    """
    if not isinstance(operator, TrigoFunctType):
        raise TypeOperatorError([TrigoFunctType], type(operator))

    if operator in [TrigoFunctType.ATAN2, TrigoFunctType.ATAN2D]:
        return f"{operator.psql}(CAST({path_op.op1} AS decimal), {path_op.op2})"

    return f"{operator.psql}(CAST({path_op.op1} AS decimal))"


def json_path_str(path_op: DotMap, operator: _OPERATORTYPE) -> str:
    """
    Get the corresponding jsonb path for a str function from a MagicDotPath.

    Args:
        path_op: path of the operand(s).
        operator: Operator Type.

    Returns:
        A path with the correct jsonb syntax.

    Raises:
        TypeOperatorError: If type of operator is not `StrFunctType`.
    """
    if not isinstance(operator, StrFunctType):
        raise TypeOperatorError([StrFunctType], type(operator))

    return f"{operator.psql}(CAST({path_op.op1} AS TEXT))"
