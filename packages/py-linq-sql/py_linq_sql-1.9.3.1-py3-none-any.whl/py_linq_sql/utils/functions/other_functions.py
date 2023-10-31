"""Functions used in py-linq-sql."""

# Standard imports
import json
import re
import secrets
import string
from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Tuple

# Third party imports
from psycopg import sql
from py_linq import Enumerable
from rich.console import Console
from rich.table import Table

# Local imports
from ...exception.exception import ColumnNameError
from ..classes.magicdotpath import BaseMagicDotPath, MagicDotPath
from ..classes.other_classes import Connection

# This regex validate column names.
# Valid column names begin by a  letter (upper or lower case) and is followed by
# letter (upper of lower case), number and/or '_' between 2 and 57 characters.
_COL_NAME_PATTERN = re.compile(r"^[a-zA-Z][0-9a-zA-Z_]{2,57}$")


def _col_name_validator(name: str) -> str:
    """
    Validate or not a custom column name.

    A valid column name begins by a letter and is followed by letter, number or '_'.
    [a-zA-Z0-9_]
    The max size of a column name is 63 bytes for the database.
    Here we limit it to 58 bytes because we keep 1 bytes for a potential
    prefix of psql and4 bytes for a suffix if there are several identical column names.

    Args:
        name: column name to validate.

    Returns:
        name if all is good.

    Raises:
        ColumnNameError: If the column name is invalid.
        re.error: Indirect raise by `re.compile` or `re.match`.

    Examples:
        Valid column names:

        >>> _col_name_validator("toto")
        toto
        >>> _col_name_validator("Toto")
        Toto
        >>> _col_name_validator("toto8")
        toto8
        >>> _col_name_validator("Toto8")
        Toto8
        >>> _col_name_validator("toto_titi")
        toto_titi
        >>> _col_name_validator("Toto_titi")
        Toto_titi
        >>> _col_name_validator("toto_8")
        toto_8
        >>> _col_name_validator("Toto_8")
        Toto_8
        >>> _col_name_validator("toto_8_titi")
        toto_8_titi
        >>> _col_name_validator("Toto_8_titi")
        Toto_8_titi

        Invalid column names:
        >>> try:
        ...     _col_name_validator("_toto")
        ... except(ColumnNameError):
        ...     print("error")
        "error"

        >>> try:
        ...     _col_name_validator("8toto")
        ... except(ColumnNameError):
        ...     print("error")
        "error"

        >>> try:
        ...     _col_name_validator("toto*")
        ... except(ColumnNameError):
        ...     print("error")
        "error"

        >>> try:
        ...     _col_name_validator(
        ...         "48_degrees_51_minutes_45_81_seconds_N_2_degrees_17_"
        ...         "minutes_15_331_seconds_E",
        ...     )
        ... except(ColumnNameError):
        ...     print("error")
        "error"
    """
    if not _COL_NAME_PATTERN.match(name):
        raise ColumnNameError(name)

    return name


def _fix_same_column_name(names: List[str]) -> List[str]:
    """
    Fix names of columns.

    If we have column with the same name, suffix column with '__n'.

    Args:
        names: Columns name.

    Returns:
        Columns name suffixed if it necessary.

    Examples:
        >>> _fix_same_column_name(['toto', 'titi', 'toto', 'tutu', '8_add_titi'])
        ['toto', 'titi', 'toto__1', 'tutu', '_8_add_titi']
    """
    result = []
    tmp_dict = {name: 0 for name in names}

    for name in names:
        new_name = f"{name}__{tmp_dict[name]}" if tmp_dict[name] > 0 else name
        result.append(new_name if new_name[0].isalpha() else f"_{new_name}")
        tmp_dict[name] += 1

    return result


def _get_random_string(number: int) -> str:
    """
    Get a random string.

    See:
        https://stackoverflow.com/questions/2257441/
        random-string-generation-with-upper-case-letters-and-digits/23728630#23728630

    Args:
        number: The size of the return string.

    Returns:
        A Random string with a size equal to number.
    """
    return "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(number)
    )


def _short_columns_default_name(col_name: str) -> str:
    """
    Shot a column name with a random string at the end.

    Args:
        col_name: string to short.

    Returns:
        Column name with a random string at the end with a len <= 58.

    Examples:
        >>> size = len(_short_columns_default_name(
        ...     "x_data_obj_name_add_1_add_2_add_3_add_4_add_5_add_6_add_7_add_8_add_9"
        ... ))
        >>> size <= 58
        True
    """
    return f"{col_name[0:48]}{_get_random_string(10)}"


def get_columns_name(
    mdps: MagicDotPath
    | List[MagicDotPath]
    | Tuple[MagicDotPath]
    | Dict[str, MagicDotPath],
) -> List[str]:
    """
    Get all column name.

    Args:
        mdps: MagicDotPath for which we want the column name.

    Returns:
        All of paths and columns.

    Raises:
        TypeOperatorError: Indirect raise by `MagicDotPathWithOp.col_name`.
    """
    result = []

    match mdps:
        case BaseMagicDotPath():
            col_name = mdps.col_name()
            result.append(
                f"_{_short_columns_default_name(col_name)}"
                if len(col_name) > 58
                else f"{col_name}",
            )
        case tuple() | list():
            for element in mdps:
                col_name = element.col_name()
                result.append(
                    f"_{_short_columns_default_name(col_name)}"
                    if len(col_name) > 58
                    else f"{col_name}",
                )
        case dict():
            for key in mdps:
                result.append(_col_name_validator(key))

    return _fix_same_column_name(result)


def get_good_type(cast_type: type) -> str | None:
    """
    Get the good type as str from a cast_type.

    Args:
        cast_type: Type in which we want to cast the path.

    Returns:
        SQL type with '))' to cast in sql command. None if we give the wrong type.
    """
    if cast_type in (int, float, Decimal):
        return "decimal))"
    if cast_type == date:
        return "date))"
    return None


def get_json(data: Dict[Any, Any]) -> str:
    """
    Get a json from data.

    Args:
        data: data we want to have in json.

    Returns:
        A json contains data.

    Raises:
        ValueError: Indirect raise by `json.dumps`.
    """
    return json.dumps(data)


def pretty_print(record: Enumerable) -> None:
    """
    Print a record in a pretty table with rich.

    Args:
        record: Record to display.

    Raises:
        rich.errors.ConsoleError: Indirect raise by `rich.table`
        rich.console.CaptureError: Indirect raise by `rich.console`
    """
    if record is None:
        Console().print("Record is None.")
    else:
        rec_in_list = record.to_list()
        if not rec_in_list:
            Console().print("Empty Enumerable.")
        else:
            table = Table(title="Record", show_lines=True)

            for name in rec_in_list[0]._fields:
                table.add_column(name, justify="center", no_wrap=True)

            for element in rec_in_list:
                table.add_row(*map(str, element))

            Console().print(table)
            count = len(rec_in_list)
            row_repr = f"({count} rows)" if count > 1 else f"({count} row)"
            Console().print(row_repr)


def safe(connection: Connection, name: str) -> str:
    """
    Secure a column or a table for a request.

    Args:
        name: Name of the column or table we want to secure.

    Returns:
        Name but verified by psycopg.sql.Identifier.

    Raises:
        psycopg.Error: Indirect raise by `sql.Identifier` or `as_string`.
    """
    return sql.Identifier(name).as_string(connection)
