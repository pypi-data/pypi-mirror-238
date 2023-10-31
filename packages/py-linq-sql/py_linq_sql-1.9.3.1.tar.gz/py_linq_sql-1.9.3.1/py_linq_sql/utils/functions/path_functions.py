"""Path functions used in py-linq-sql."""

# Standard imports
import re
from typing import Dict, List, Tuple

# Local imports
from ...exception.exception import TableError
from ..classes.enum import CommandType
from ..classes.magicdotpath import (
    BaseMagicDotPath,
    LambdaMagicDotPath,
    MagicDotPath,
    MagicDotPathWithOp,
)
from ..classes.other_classes import SQLEnumerableData


def _check_table(sqle: SQLEnumerableData, magic_dp: MagicDotPath) -> None:
    """
    Check if the given table of the magic_dp is in the list of table in the join.

    Args:
        sqle: SQLEnumerable contains the join commands.
        magic_dp: MagicDotPath to check.

    Raises:
        TableError: If the first attribute of the magic_dp is not in
        the list of table in join command.
    """
    for cmd in sqle.cmd:
        if cmd.cmd_type in [CommandType.JOIN, CommandType.GROUP_JOIN]:
            join_command = cmd
            break

    outer = join_command.args.outer
    inner = join_command.args.inner

    tables = [outer.table[1:-1], inner.table[1:-1]]

    if magic_dp.with_table not in tables:
        raise TableError(magic_dp.attributes[0], tables)


def _get_path_base_mdp(
    magic_dp: BaseMagicDotPath,
    sqle: SQLEnumerableData | None,
    force: bool,
    paths: List[str],
) -> None:
    """
    Get a path for a BaseMagicDotPath.

    Args:
        magic_dp: MagicDotPath from which we want to get the path.
        sqle: SQLEnumerableData with connection, flags, list of commands and a table.
        force: True to force the path in str, False otherwise.
        paths: All generate paths previously.

    Raises:
        TypeError: If magic_dp is not a subclass of BaseMagicDotPath.
        psycopg.Error: Indirect raise by `MagicDotPath.jsonb_path`
            or `MagicDotPathWithOp.jsonb_path`.
        TableError: Indirect raise by `_check_table`
    """
    match magic_dp:
        case MagicDotPath():
            if sqle and sqle.flags.join:
                magic_dp.with_table = magic_dp.attributes[0][1:-1]
                del magic_dp.attributes[0]
                _check_table(sqle, magic_dp)
            paths.append(magic_dp.jsonb_path(force))
        case MagicDotPathWithOp():
            type_error = True
            if sqle and sqle.flags.join:
                operand_1, operand_2 = magic_dp.operand_1, magic_dp.operand_2
                if isinstance(operand_1, MagicDotPath):
                    operand_1.with_table = operand_1.attributes[0][1:-1]
                    del operand_1.attributes[0]
                    _check_table(sqle, operand_1)
                    type_error = False
                if isinstance(operand_2, MagicDotPath):
                    operand_2.with_table = operand_2.attributes[0][1:-1]
                    del operand_2.attributes[0]
                    _check_table(sqle, operand_2)
                    type_error = False
                # Ignore the coverage because is just an other security,
                # but the exception was raised before.
                if type_error:  # pragma: no cover
                    raise TypeError("Operand_1 or Operand_2 must be BaseMagicDotPath.")
            paths.append(magic_dp.jsonb_path(force))
        case _:
            raise TypeError(
                "`get_path()` take only BaseMagicDotPath.",
            )


def get_path(
    magic_dp: BaseMagicDotPath | Tuple[BaseMagicDotPath] | Dict[str, BaseMagicDotPath],
    sqle: SQLEnumerableData | None = None,
    force: bool = False,
) -> List[str]:
    """
    Get path from a MagicDotPath.

    Args:
        magic_dp: A MagicDotPath objects contains a bases with element of the future
            path.
        sqle: SQLEnumerableData with connection, flags, list of commands and a table.
        force: True if we want to force the json path in text, False otherwise.
            By default: False.

    Returns:
        List a path transform by jsonb_path.

    Raises:
        TypeError: If magic_dp is not a subclass of BaseMagicDotPath.
        psycopg.Error: Indirect raise by `_get_path_base_mdp`.
        TableError: Indirect raise by `_get_path_base_mdp`.
    """
    paths: List[str] = []

    match magic_dp:
        case BaseMagicDotPath():
            _get_path_base_mdp(magic_dp, sqle, force, paths)
        case tuple():
            for element in magic_dp:
                _get_path_base_mdp(element, sqle, force, paths)
        case dict():
            for element in magic_dp.values():
                _get_path_base_mdp(element, sqle, force, paths)
        case _:
            raise TypeError(
                "`get_path()` take only BaseMagicDotPath or tuple of BaseMagicDotPath.",
            )

    return paths


def get_paths(
    fquery: LambdaMagicDotPath,
    sqle: SQLEnumerableData,
    as_str: bool = False,
) -> List[str]:
    """
    Get jsonb paths to build commands.

    The format of paths give by the function: person->'address'->'zip_code'

    Args:
        fquery: Lambda function to get the path(s)
        sqle: SQLEnumerableData with connection, flags, list of commands and a table.
        as_str: False if we want basic paths, True if we want force the paths on string.

    Returns:
        List of paths.

    Raises:
        psycopg.Error: Indirect raise by `get_path`.
        TableError: Indirect raise by `get_path`.
        TypeError: Indirect raise by `get_path`.
        TypeOperatorError: Indirect raise by `BaseMagicDotPath._get_number_operator`
            or `BaseMagicDotPath._get_generic_operator`.
    """
    return get_path(fquery(MagicDotPath(sqle.connection)), sqle, as_str)


def get_update_path(path: str) -> str:
    """
    Get the correct format of path for UPDATE.

    We need a path like: `{0, 1, 2, 3}`.

    Args:
        path: The path to get in the correct format for UPDATE.

    Returns:
        The path in the correct format for UPDATE.
    """
    tmp = re.split(r">|-|'", path)

    # Delete the first, is the column
    tmp = tmp[1:]

    # Join all not None str in tmp with the function filter()
    # (https://docs.python.org/3/library/functions.html#filter)
    result = ",".join(filter(None, tmp))

    return "{" + result + "}"
