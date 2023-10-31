"""Enum used in py-linq-sql."""

# Future imports
from __future__ import annotations

# Standard imports
import sys
from collections import namedtuple
from enum import Enum, auto
from typing import TypeAlias

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

# ----------------
# |  NamedTuple  |
# ----------------

_Type = namedtuple("_Type", ["is_intersect", "as_str"])

# ----------
# |  Enum  |
# ----------


class CommandType(StrEnum):
    """Enum of command type."""

    SELECT = "select"
    WHERE = "where"
    MIN = "min"
    MAX = "max"
    INSERT = "insert"
    ORDER_BY = "order by"
    ORDER_BY_DESC = "order by desc"
    TAKE = "take"
    SKIP = "skip"
    ELEMENT_AT = "element at"
    FIRST = "first"
    UPDATE = "update"
    COUNT = "count"
    SINGLE = "single"
    LAST = "last"
    TAKE_LAST = "take last"
    SKIP_LAST = "skip last"
    ALL = "all"
    ANY = "any"
    CONTAINS = "contains"
    EXCEPT_ = "except"
    JOIN = "join"
    UNION = "union"
    INTERSECT = "intersect"
    DISTINCT = "distinct"
    GROUP_BY = "group by"
    DELETE = "delete"
    GROUP_JOIN = "group join"


# HACK: It's a new type for mypy. The time that mypy supports the Strenum.
# https://github.com/python/mypy/issues
CommandTypeOrStr: TypeAlias = CommandType | str


class JoinType(_Type, Enum):
    """Enum of join type."""

    INNER = _Type(is_intersect=False, as_str="INNER")
    LEFT = _Type(False, "LEFT")
    LEFT_MINUS_INTERSECT = _Type(True, "LEFT")
    RIGHT = _Type(False, "RIGHT")
    RIGHT_MINUS_INTERSECT = _Type(True, "RIGHT")
    FULL = _Type(False, "FULL")
    FULL_MINUS_INTERSECT = _Type(True, "FULL")


class Terminal(Enum):
    """Enum of state of terminal flags."""

    COUNT = auto()
    DISTINCT = auto()
    ELEMENT_AT = auto()
    EXCEPT_ = auto()
    INTERSECT = auto()
    LAST = auto()
    MAX = auto()
    MIN = auto()
    SINGLE = auto()
    UNION = auto()
    GROUP_BY = auto()
    GROUP_JOIN = auto()
