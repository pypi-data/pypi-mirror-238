"""Code of the project py-linq-sql."""

__version__ = "1.8.3-pre-release"

# Local imports

# Local imports
from .build_request.consult_aggregate import (  # noqa: F401
    avg,
    concat,
    count,
    max,
    min,
    sum,
)
from .exception.exception import (  # noqa: F401
    ActionError,
    AlreadyExecutedError,
    AlterError,
    ColumnNameError,
    CursorCloseError,
    DatabError,
    DeleteError,
    EmptyInputError,
    EmptyQueryError,
    EmptyRecordError,
    ExecutionError,
    FetchError,
    GroupByWithJoinError,
    LengthMismatchError,
    MoreThanZeroError,
    NeedSelectError,
    NeedWhereError,
    NegativeNumberError,
    NoMaxOrMinAfterLimitOffsetError,
    OneError,
    OtherThanWhereError,
    PSQLConnectionError,
    PyLinqSQLError,
    ReadOnlyPermissionDeniedError,
    ReturnEmptyEnumerable,
    SelectError,
    TableError,
    TablePermissionDeniedError,
    TerminalError,
    TooManyReturnValueError,
    TypeOperatorError,
    UnknownCommandTypeError,
)
from .sql_enumerable.sql_enumerable import SQLEnumerable  # noqa: F401
from .utils.classes.enum import JoinType  # noqa: F401
from .utils.classes.other_classes import PyLinqSqlInsertType  # noqa: F401
from .utils.db import connect  # noqa: F401
from .utils.execute import logg  # noqa: F401
from .utils.functions.magic_dp_hyperb_functions import (  # noqa: F401
    acosh,
    asinh,
    atanh,
    cosh,
    sinh,
    tanh,
)
from .utils.functions.magic_dp_maths_functions import (  # noqa: F401
    cbrt,
    ceil,
    degrees,
    exp,
    factorial,
    floor,
    gcd,
    lcm,
    ln,
    log,
    log10,
    min_scale,
    radians,
    round,
    scale,
    sign,
    sqrt,
    trim_scale,
    trunc,
)
from .utils.functions.magic_dp_other_functions import is_in  # noqa: F401
from .utils.functions.magic_dp_str_functions import lower, title, upper  # noqa: F401
from .utils.functions.magic_dp_trigo_functions import (  # noqa: F401
    acos,
    acosd,
    asin,
    asind,
    atan,
    atan2,
    atan2d,
    atand,
    cos,
    cosd,
    cot,
    cotd,
    sin,
    sind,
    tan,
    tand,
)
from .utils.functions.other_functions import pretty_print  # noqa: F401
