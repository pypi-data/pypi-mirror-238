"""Build all alter commands."""

# Standard imports
from decimal import Decimal
from types import NoneType
from typing import Any, Dict, List, Set, Tuple

# Local imports
from ..exception.exception import DeleteError, NeedWhereError, TooManyReturnValueError
from ..utils.classes.magicdotpath import MagicDotPath
from ..utils.classes.other_classes import Command, SQLEnumerableData
from ..utils.functions.other_functions import get_json
from ..utils.functions.path_functions import get_path, get_update_path
from .consult import build_where


def build_delete(
    command: Command,
    sqle: SQLEnumerableData,
    built_commands: Set[int],
) -> str:
    """
    Build a delete request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        built_commands: All commands that have already been built.

    Returns:
        Request to execute.

    Raises:
        DeleteError: If len(sqle.cmd) > 1 and command.args.armageddon).
        NeedWhereError: If len(sqle.cmd) < 2.
        psycopg.Error: Indirect raise by `build_where`.
        TableError: Indirect raise by `build_where`.
        TypeError: Indirect raise by `build_where`.
        TypeOperatorError: Indirect raise by `build_where`.
    """
    armageddon = command.args.armageddon

    result = [f"DELETE FROM {sqle.table}"]

    if len(sqle.cmd) > 1 and armageddon:
        raise DeleteError("where")

    if armageddon:
        return result[0]

    if len(sqle.cmd) < 2:
        raise NeedWhereError()

    result.append(build_where(sqle, built_commands))

    # We use filter with None for the argument __function.
    # If we give None to the first element of filter
    # it will pass all the elements evaluate to false no matter why.
    #
    # We can have None in result if sqle.cmd contains commands
    # which will be evaluated later in build_where()
    return " ".join(filter(None, result))


def _build_array_from_list_or_tuple(data: Tuple[Any, ...]) -> List[str]:
    """
    Build an SQL Array from a List or form a tuple.

    Args:
        data: Data to transform in array.

    Returns:
        Sub request to execute.
    """
    result = []

    build_simple_type = _build_values_for_insert_simple_type

    for val in data:
        match val:
            case str():
                result.append(f"'{str(val)}'")
            case list() | tuple():
                result.append(
                    f"ARRAY [{', '.join([build_simple_type(v) for v in val])}]",
                )
            case dict():
                result.append(f"('{get_json(val)}')")
            case NoneType():
                result.append("Null")
            case _:
                result.append(str(val))

    return result


def _build_values_for_insert_tuple(data: Tuple[Any, ...]) -> str:
    """
    Build values for insert if data is a tuple.

    Args:
        - data: data to build for the insert.

    Returns:
        Sub request to execute.

    Raises:
        TypeError: Raise when the data had the wrong type.
        ValueError: Indirect raise by `_build_array_from_list_or_tuple`.
    """
    return f"( {', '.join(_build_array_from_list_or_tuple(data))} )"


def _build_values_for_insert_list(
    data: List[Tuple[Any, ...]] | List[Dict[str, Any]],
) -> str:
    """
    Build values for insert if data is a list.

    If data is a list, this means that we insert several lines. So tuple for relational
    insert or mixed insert or dict for json insert.

    Args:
        - data: data to build for the insert.

    Returns:
        Sub request to execute.

    Raises:
        TypeError: Raise when the data had the wrong type.
        ValueError: Indirect raise by `_build_values_for_insert_simple_type`
            or `_build_values_for_insert_tuple`.
    """
    result = []

    for val in data:
        match val:
            case tuple():
                result.append(_build_values_for_insert_tuple(val))
            case dict():
                result.append(_build_values_for_insert_simple_type(val))
            case _:
                raise TypeError(
                    "In a multi insert (list), you can just put tuple, "
                    f"line for relational or mixed, or dict for json not {type(val)}",
                )

    return ", ".join(result)


def _build_values_for_insert_simple_type(
    data: Dict[str, Any] | str | int | float | Decimal,
) -> str:
    """
    Build simple type value ofr insert.

    Args:
        - data: data to build for the insert.

    Returns:
        Sub request to execute.

    Examples:
        >>> _build_values_for_insert_simple_type("hello world")
        "('hello world')"

        >>> res = r'''('{"a": "aa", "b": {"bb": "bbb"}}')'''
        >>> _build_values_for_insert_simple_type({"a": "aa", "b": {"bb": "bbb"}}) == res
        True

        >>> _build_values_for_insert_simple_type(12)
        '12'

        >>> _build_values_for_insert_simple_type(12.05)
        '12.05'

    """
    match data:
        case dict():
            return f"('{get_json(data)}')"
        case str():
            return f"('{str(data)}')"
        case NoneType():
            return "Null"
        case _:
            return str(data)


def build_insert(command: Command, sqle: SQLEnumerableData) -> str:
    """
    Build an insert request for json table or relational table.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.

    Returns:
        Request to execute.

    Raises:
        TypeError: Raise when the data had the wrong type or
            Indirect raise by `_build_json_insert`.
        ValueError: Indirect raise by `_build_values_for_insert_simple_type`
            or `_build_values_for_insert_list`.
    """
    column = command.args.column
    data = command.args.data

    result = [f"INSERT INTO {sqle.table}("]

    match column:
        case str():
            result.append(f"{column}")
            result.append(")")
        case _:
            result.append(", ".join(column))
            result.append(")")

    result.append("VALUES")

    match data:
        case tuple():
            result.append(_build_values_for_insert_tuple(data))
        case list():
            result.append(_build_values_for_insert_list(data))
        case _:
            result.append(_build_values_for_insert_simple_type(data))

    return " ".join(result)


def build_update(
    command: Command,
    sqle: SQLEnumerableData,
    built_commands: Set[int],
) -> str:
    """
    Build an update request.

    Args:
        command: Command to build.
        sqle: SQLEnumerable with connection, flags, list of commands and a table.
        built_commands: All commands that have already been built.

    Returns
        Request to execute.

    Raises:
        TooManyReturnValueError: If len of path > 1.
        psycopg.Error: Indirect raise by `build_where`.
        TableError: Indirect raise by `build_where`.
        TypeError: Indirect raise by `build_where`.
        TypeOperatorError: Indirect raise by `build_where`,
            `BaseMagicDotPath._get_number_operator`
            or `BaseMagicDotPath._get_generic_operator`.
    """
    fquery = command.args.fquery  # pylint: disable=duplicate-code
    mdp_w_path = fquery(MagicDotPath(sqle.connection))
    path = get_path(mdp_w_path, sqle)

    if len(path) > 1:
        raise TooManyReturnValueError("Update")

    operand_1 = mdp_w_path.operand_1
    column = operand_1.column
    operand_2 = mdp_w_path.operand_2

    json = len(operand_1.attributes) > 1
    path_for_update = "-".join(operand_1.attributes[1:])

    result = [f"UPDATE {sqle.table} SET {column} ="]

    if json:
        result.append(
            f"""jsonb_set({column}, """
            f"""'{get_update_path(path_for_update)}'::text[], '""",
        )

    match operand_2:
        case str() if not json:
            result.append(f"'{operand_2}'")
        case str() if json:
            result.append(f'"{operand_2}"')
        case _:
            result.append(f"{operand_2}")

    if json:
        result.append("', false)")

    if len(sqle.cmd) > 1:
        result.append(build_where(sqle, built_commands))

    # We use filter with None for the argument __function.
    # If we give None to the first element of filter
    # it will pass all the elements evaluate to false no matter why.
    #
    # We can have None in result if sqle.cmd contains commands
    # which will be evaluated later in build_where()
    return " ".join(filter(None, result))
