"""Functions to manage the configuration of py-linq-sql."""
# Standard imports
from functools import lru_cache
from typing import Any, Iterable, cast

# Third party imports
import toml
import yaml


def _load_config_file(
    toml_file: str | None = ".pylinqsql-conf.toml",
    yaml_file: str | None = ".pylinqsql-conf.yaml",
    pyproject_file: str | None = "pyproject.toml",
) -> dict[str, Any]:
    """
    Load a config file for py-linq-sql.

    First we try to load '.pylinqsql-conf.toml',
    if the toml file does not exist we try to load '.pylinqsql-conf.yaml'
    finally if none of these files exist we try to load 'pyproject.toml'.

    Function arguments are only useful for testing.
    In real conditions we use the files described above.

    Args:
        toml_file: Toml config file.
        yaml_file: Yaml config file.
        pyproject_file: Pyproject config file.

    Returns:
        Config with whitelist, blacklist and readonly if it is specified in the config
        files,
        otherwise return {"whitelist": None, "blacklist": None, "readonly": False}.

    Raises:
        IOerror: Indirect raise by `open`.
        TypeError: Indirect raise by `toml.load`.
        TomlDecodeError: Indirect raise by `toml.load`.
        YAMLError: Indirect raise by `yaml.safe_load`.
    """
    config = {"whitelist": None, "blacklist": None, "readonly": False}

    try:
        loaded = toml.load(cast(str, toml_file))
        config = loaded.get(
            "pylinqsql",
            {"whitelist": None, "blacklist": None, "readonly": False},
        )
    except FileNotFoundError:
        try:
            with open(cast(str, yaml_file), "r", encoding="utf-8") as file:
                loaded = yaml.safe_load(file)
                if not loaded:
                    config = {"whitelist": None, "blacklist": None, "readonly": False}
                else:
                    config = loaded.get(
                        "pylinqsql",
                        {"whitelist": None, "blacklist": None, "readonly": False},
                    )
        except FileNotFoundError:
            try:
                pyproject_conf = toml.load(cast(str, pyproject_file))["tool"]
                config = pyproject_conf.get(
                    "pylinqsql",
                    {"whitelist": None, "blacklist": None, "readonly": False},
                )
            except FileNotFoundError:
                config = {"whitelist": None, "blacklist": None, "readonly": False}

    return config


@lru_cache(maxsize=1)
def _get_config(
    config_for_test: str | None = None,
) -> dict[str, list[str | None] | None | bool]:
    """
    Get the config from a config file.

    Function arguments are only useful for testing.
    In real conditions we use the files described in `_load_config_file`.

    Args:
        config_for_test: A config for testing the function.

    Returns:
        Config with whitelist, blacklist and readonly if it is specified in the config
        files,
        otherwise return {"whitelist": None, "blacklist": None, "readonly": False}.

    Raises:
        IOerror: Indirect raise by `_load_config_file`.
        TypeError: Indirect raise by `_load_config_file`.
        TomlDecodeError: Indirect raise by `_load_config_file`.
        YAMLError: Indirect raise by `_load_config_file`.
    """
    if config_for_test:
        config = yaml.safe_load(config_for_test)
        if config is None:
            config = {}
    else:
        config = _load_config_file()

    white = config.get("whitelist", None)
    black = config.get("blacklist", None)
    readonly = config.get("readonly", False)

    return {
        "whitelist": white,
        "blacklist": black,
        "readonly": readonly,
    }


def is_valid_table_name_with_white_and_black_list(  # type: ignore[return]
    table_name: str,
) -> bool:
    """
    Verify if the table name is not in the black list and in the white list.

    If no (or empty) white and/or black list we treat the specific cases according to:
    black list  white list.

    See the documentation to learn more proposed specific cases.

    Args:
        table_name: The name of the table to validate.

    Returns:
        True is the table name is valid, False otherwise.
    """
    config = _get_config()

    w_list = (
        None
        if config["whitelist"] is None
        else set(cast(Iterable, config["whitelist"]))
    )
    b_list = (
        None
        if config["blacklist"] is None
        else set(cast(Iterable, config["blacklist"]))
    )

    match (w_list, b_list):
        case (None, None):
            return True
        case (None, set()) if not b_list:
            return True
        case (set(), _) if not w_list:
            return False
        case (None, _):
            return table_name not in b_list  # type: ignore[operator]
        case (_, None):
            return table_name in w_list  # type: ignore[operator]
        case _:
            return table_name in w_list - b_list  # type: ignore[operator]


def is_read_only() -> bool:
    """
    Verify if the library configuration is read only or not.

    Returns:
        True if we want denied write to database, False otherwise.
    """
    config = _get_config()
    return cast(bool, config["readonly"])
