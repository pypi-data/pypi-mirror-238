import os
import requests
import json

from .general import generate_vault_policy_name
from .exceptions import VaderGenericError

SERVICE_URL = os.environ["POLICY_SERVICE_URL"]


def create_policy(
    namespace,
    app_id,
    boundary_id,
    category,
    unique_name,
    permissions,
    description,
    version,
    allowed_projects=True,
    assignable=True,
):
    data = {
        "permissions": permissions,
        "metadata": {"description": description, "version": version},
        "allowed_projects": allowed_projects,
        "assignable": assignable,
    }
    headers = {"namespace": namespace}
    url = f"{SERVICE_URL}/{app_id}/{boundary_id}/policy/{category}/{unique_name}"
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return json.loads(response.content)

    policy_name = generate_vault_policy_name(app_id, boundary_id, category, unique_name)
    raise VaderGenericError(
        f"Could not create policy {policy_name}",
        details=str(response.text),
        status_code=response.status_code,
    )


def delete_policy(namespace, app_id, boundary_id, category, unique_name):
    url = f"{SERVICE_URL}/{app_id}/{boundary_id}/policy/{category}/{unique_name}"
    headers = {"namespace": namespace}
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {}

    policy_name = generate_vault_policy_name(app_id, boundary_id, category, unique_name)
    raise VaderGenericError(
        f"Could not delete policy {policy_name}",
        details=str(response.text),
        status_code=response.status_code,
    )


def get_policy_by_name(namespace, policy_name):
    headers = {"namespace": namespace}
    url = f"{SERVICE_URL}/policy/{policy_name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content)

    raise VaderGenericError(
        f"Could not get policy {policy_name}",
        details=str(response.text),
        status_code=response.status_code,
    )


def get_policy_by_project(namespace, app_id, boundary_id, category, unique_name):
    headers = {"namespace": namespace}
    url = f"{SERVICE_URL}/{app_id}/{boundary_id}/policy/{category}/{unique_name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content)

    policy_name = generate_vault_policy_name(app_id, boundary_id, category, unique_name)
    raise VaderGenericError(
        f"Could not get policy {policy_name}",
        details=str(response.text),
        status_code=response.status_code,
    )
