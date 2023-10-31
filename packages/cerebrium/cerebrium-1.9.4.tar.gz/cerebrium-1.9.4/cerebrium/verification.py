import re
import cerebrium.datatypes as datatypes
from cerebrium.utils import cerebriumLog, update_with_defaults


def validate_name(name: str) -> str:
    """Validate the name of the deployment"""
    message = ""
    if not name:
        message += "No name provided.\n"

    # length
    if len(name) > 32:
        message += "Name must be at most 32 characters.\n"  # TODO verify the max length

    # only allow lower case letters, numbers, and dashes
    if not re.match("^[a-z0-9\\-]*$", name):
        message += "Name must only contain lower case letters, numbers, and dashes.\n"
    return message


def validate_python_version(python_version: str) -> str:
    message = ""
    if not python_version:
        return message

    vals = [v.value for v in datatypes.PythonVersion]
    if python_version not in vals:
        message += f"Python version must be one of {vals}\n"

    return message


def validate_hardware_selection(user_hardware: str) -> str:
    message = ""
    # Check that hardware is valid and assign to enum
    if not user_hardware:
        print("No hardware provided. Defaulting to AMPERE_6000.")
        return "AMPERE_A6000"

    if user_hardware not in datatypes.Hardware.available_hardware():
        message += (
            f"Hardware must be one of:{datatypes.Hardware.available_hardware()}\n"
        )
    return message


def validate_cooldown(cooldown) -> str:
    message = ""
    if not cooldown:
        return message
    if cooldown < 0:
        message += "Cooldown must be a non-negative number of seconds.\n"
    return message


def validate_min_replicas(min_replicas) -> str:
    """Validate the minimum number of replicas"""
    message = ""
    if min_replicas is None or min_replicas == "":
        return message
    if min_replicas < 0 or not isinstance(min_replicas, int):
        message += "Minimum number of replicas must be a non-negative integer.\n"
    return message


def validate_max_replicas(max_replicas, min_replicas) -> str:
    """Validate the maximum number of replicas"""
    message = ""
    if max_replicas is None or max_replicas == "":
        return message
    if max_replicas < 1 or not isinstance(max_replicas, int):
        message += "Maximum number of replicas must be a non-negative integer greater than 0.\n"
    if max_replicas < min_replicas:
        message += "Maximum number of replicas must be greater than or equal to minimum number of replicas.\n"
    return message


def validate_and_update_cortex_params(params: dict) -> dict:
    """Validate the cortex deployment"""

    defaults = {
        "hardware": datatypes.DEFAULT_HARDWARE_SELECTION,
        "python_version": datatypes.DEFAULT_PYTHON_VERSION,
        "cooldown": datatypes.DEFAULT_COOLDOWN,
        "min_replicas": datatypes.DEFAULT_MIN_REPLICAS,
        "cpu": datatypes.DEFAULT_CPU,
        "hide_public_endpoint": False,
    }
    params = update_with_defaults(params=params, defaults=defaults)

    message = ""
    message += validate_name(params["name"])
    message += validate_hardware_selection(params["hardware"])
    message += validate_python_version(params["python_version"])
    message += validate_cooldown(params["cooldown"])
    message += validate_min_replicas(params["min_replicas"])
    if "max_replicas" in params:
        message += validate_max_replicas(params["max_replicas"], params["min_replicas"])

    hardware_option = getattr(datatypes.Hardware, params["hardware"])

    if params.get("gpu_count") is None:
        params["gpu_count"] = 1 if params["hardware"] != "CPU" else 0
    if params.get("memory") is None:
        params["memory"] = (
            datatypes.DEFAULT_MEMORY
            if params["hardware"].upper() != "CPU"
            else params["cpu"] * hardware_option.max_memory_per_cpu
        )

    message += hardware_option.validate(
        cpu=params["cpu"], memory=params["memory"], gpu_count=params["gpu_count"]
    )

    if message:
        cerebriumLog(message=message, level="ERROR")

    return params
