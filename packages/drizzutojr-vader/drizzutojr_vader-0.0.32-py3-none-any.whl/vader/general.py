import re
import copy

from pathlib import Path

from .exceptions import *

SPECIAL_CHARACTERS = "[-@!#$%^&*()<>?/\\\|}{~:]"
BLACKLIST_KEYS = ["password", "token", "secret_id", "secret-id", "credential"]
SANITIZE_VALUE = "SANITIZE"


def contains_special_character(
    custom_string: str, special_characters: str = SPECIAL_CHARACTERS
):
    regex = re.compile(special_characters)
    if regex.search(custom_string):
        return True
    return False


def generate_project_name(app_id, boundary_id):
    return f"{app_id}-{boundary_id}"


def generate_namespace_path(parent_namespace, namespace):
    return f"{parent_namespace}/{namespace}".replace("//", "/")


def generate_full_path(namespace_path, parent_path, resource_name):
    return f"{namespace_path}/{parent_path}/{resource_name}".replace("//", "/")


def generate_vault_policy_name(app_id, boundary_id, category, unique_name):
    return f"{app_id}-{boundary_id}-{category}-{unique_name}"


def sanitize_dict(the_dict, whitelist_keys=[], blacklist_keys=[]):
    the_dict = copy.deepcopy(the_dict)
    blacklist_keys = list(set(blacklist_keys + BLACKLIST_KEYS))
    blacklist_keys = list(filter(lambda x: x not in whitelist_keys, blacklist_keys))

    for key, value in the_dict.items():
        if isinstance(value, dict):
            the_dict[key] = sanitize_dict(value, whitelist_keys, blacklist_keys)
        elif key.lower() in blacklist_keys:
            the_dict[key] = SANITIZE_VALUE

    return the_dict


def convert_to_seconds(time: str):
    try:
        integer = int(time[:-1])
    except ValueError:
        raise VaderConfigError(
            f"Time value {time} is not in valid Vader format",
            details="valid format is XXm, XXh, XXd",
        )
    if time.endswith("m"):
        return convert_mins_to_seconds(time)
    elif time.endswith("h"):
        return convert_hours_to_seconds(time)
    elif time.endswith("d"):
        return convert_days_to_seconds(time)
    else:
        raise VaderConfigError(
            f"Time value {time} is not in valid Vader format",
            details="valid format is XXm, XXh, XXd",
        )


def convert_mins_to_seconds(mins: str):
    mins = int(mins.rstrip("m"))
    return mins * 60


def convert_hours_to_seconds(hours):
    hours = int(hours.rstrip("h"))
    return hours * 60 * 60


def convert_days_to_seconds(days: str):
    days = int(days.rstrip("d"))
    return days * 24 * 60 * 60


def is_owned_by_project_compare_parts(
    app_id: str, boundary_id: str, vader_config: dict
):
    passed_project_name = generate_project_name(app_id, boundary_id)
    config_project_name = generate_project_name(
        vader_config["app_id"], vader_config["boundary_id"]
    )

    if passed_project_name == config_project_name:
        return True

    return False


def is_owned_by_project_compare_project(project_name: str, vader_config: dict):
    config_project_name = vader_config["project"]

    if project_name == config_project_name:
        return True

    return False


def is_allowed_project_compare_project(project_name: str, vader_config: dict):
    if "allowed_projects" not in vader_config.keys():
        return False

    if project_name in vader_config["allowed_projects"]:
        return True

    return False


def populate_policy_template(policy_file_path, key_values):
    template_policy = Path(policy_file_path).read_text()
    for key, value in key_values.items():
        template_policy = template_policy.replace(f"{{{key}}}", value)
    return template_policy
