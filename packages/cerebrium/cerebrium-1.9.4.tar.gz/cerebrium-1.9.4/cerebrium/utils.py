import hashlib
import os
import sys
import tempfile
import yaml
import fnmatch
from termcolor import colored

env = os.getenv("ENV", "prod")


def determine_includes(include, exclude):
    include_set = include.strip("[]").split(",")
    include_set.extend(
        [
            "./main.py",
            "./requirements.txt",
            "./pkglist.txt",
            "./conda_pkglist.txt",
        ]
    )
    include_set = set(map(ensure_pattern_format, include_set))
    include_set = [i.strip() for i in include_set]

    exclude_set = exclude.strip("[]").split(",")
    exclude_set = [e.strip() for e in exclude_set]
    exclude_set = set(map(ensure_pattern_format, exclude_set))

    file_list = []
    for root, _, files in os.walk("./"):
        for file in files:
            full_path = os.path.join(root, file)
            if any(
                fnmatch.fnmatch(full_path, pattern) for pattern in include_set
            ) and not any(
                fnmatch.fnmatch(full_path, pattern) for pattern in exclude_set
            ):
                print(f"➕ Adding {full_path}")
                file_list.append(full_path)
    return file_list


def get_api_key():
    config_path = os.path.expanduser("~/.cerebrium/config.yaml")
    msg = (
        "Please login using 'cerebrium login <private_api_key>' "
        "or specify the key using the `--api-key` flag."
    )
    if not os.path.exists(config_path):
        cerebriumLog(level="ERROR", message=msg)

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    if env == "dev":
        print("❗️❗️Logging in with dev API key❗️❗️")
        key_name = "dev_api_key"
    else:
        key_name = "api_key"

    if config is None or key_name not in config:
        cerebriumLog(level="ERROR", message=msg)

    return config[key_name]


def ensure_pattern_format(pattern):
    if not pattern.startswith("./"):
        pattern = f"./{pattern}"
    elif pattern.startswith("/"):
        cerebriumLog(
            prefix="ValueError",
            level="Error",
            message="Pattern cannot start with a forward slash. Please use a relative path.",
        )
    if pattern.endswith("/"):
        pattern = f"{pattern}*"
    elif os.path.isdir(pattern) and not pattern.endswith("/"):
        pattern = f"{pattern}/*"
    return pattern


def cerebriumLog(
    message: str,
    prefix: str = "",
    level: str = "INFO",
    attrs: list = [],
    color: str = "",
    end="\n",
):
    """User friendly coloured logging

    Args:
        message (str): Error message to be displayed
        prefix (str): Prefix to be displayed. Defaults to empty.
        level (str): Log level. Defaults to "INFO".
        attrs (list, optional): Attributes for colored printing. Defaults to None.
        color (str, optional): Color to print in. Defaults depending on log level.
        end (str, optional): End character. Defaults to "\n".
    """

    level = level.upper()
    default_prefixes = {"INFO": "Info: ", "WARNING": "Warning: ", "ERROR": "Error: "}
    default_colors = {"INFO": None, "WARNING": "yellow", "ERROR": "red"}
    prefix = prefix or default_prefixes.get(level, "")

    # None is default for unused variables to avoid breaking termcolor
    color = color or default_colors.get(level, "")

    print(colored(f"{prefix}", color=color, attrs=["bold"]), end=end)
    print(colored(f"{message}", color=color, attrs=attrs))

    if level == "ERROR":
        sys.exit(1)


def update_with_defaults(params: dict, defaults: dict):
    for key, val in defaults.items():
        if params.get(key) is None or params.get(key) == "":
            params[key] = val

    return params


def assign_param(param_dict: dict, key, new_value, default_value=None):
    param_dict[key] = (
        new_value if is_valid(new_value) else param_dict.get(key, default_value)
    )
    return param_dict


def is_valid(v):
    return (
        (isinstance(v, bool) and v is False) or bool(v) or isinstance(v, (int, float))
    )


def remove_null_values(param_dict: dict):
    return {
        key: val
        for key, val in param_dict.items()
        if (val is not None or (isinstance(val, str) and val != ""))
    }


def content_hash(files) -> str:
    """
    Hash the content of each file, avoiding metadata.
    """

    files = files if isinstance(files, list) else [files]
    if files:
        h = hashlib.sha256()
        for file in files:
            if os.path.exists(file):
                with open(file, "rb") as f:
                    h.update(f.read())
            else:
                return "FILE_DOESNT_EXIST"
        return h.hexdigest()
    return "NO_FILES"


def run_pyflakes(
    dir="",
    files=[],
    print_warnings=True,
):
    import pyflakes.api
    from pyflakes.reporter import Reporter

    with tempfile.TemporaryDirectory() as tmp:
        warnings_log_file = os.path.join(tmp, "warnings.log")
        errors_log_file = os.path.join(tmp, "errors.log")

        with open(errors_log_file, "w") as warnings_log, open(
            warnings_log_file, "w"
        ) as errors_log:
            reporter = Reporter(warningStream=warnings_log, errorStream=errors_log)
            if dir:
                pyflakes.api.checkRecursive([dir], reporter=reporter)
            elif files:
                for filename in files:
                    if os.path.splitext(filename)[1] != ".py":
                        continue
                    code = open(filename, "r").read()
                    pyflakes.api.check(code, filename, reporter=reporter)

        with open(warnings_log_file, "r") as f:
            warnings = f.readlines()

        with open(errors_log_file, "r") as f:
            errors = f.readlines()

    filtered_errors = []
    for e in errors:
        if e.count("imported but unused") > 0:
            warnings.append(e)
        else:
            filtered_errors.append(e)

    if warnings and print_warnings:
        warnings_to_print = "".join(warnings)
        cerebriumLog(
            prefix="Warning: Found the following warnings in your files.",
            message=f"\n{warnings_to_print}",
            level="WARNING",
        )

    if filtered_errors:
        errors_to_print = "".join(filtered_errors)
        cerebriumLog(
            prefix="Error: Found the following syntax errors in your files:",
            message=f"{errors_to_print}"
            "Please fix the errors and try again. \nIf you would like to ignore these errors and deploy anyway, use the `--disable-syntax-check` flag.",
            level="ERROR",
        )
    return errors, warnings
