import json

from vapi import VAPI

from abc import ABC, abstractmethod


class VaultResource(ABC):
    def _get_vault_resource(self, path, wrap_response=None):
        return VAPI().get(path, wrap_response=wrap_response)

    def _post_vault_resource(self, path, data, wrap_response=None):
        return VAPI().post(path, data=data, wrap_response=wrap_response)

    def _delete_vault_resource(self, path):
        return VAPI().delete(path)

    def _list_vault_resources(self, path, wrap_response=None):
        return VAPI().list(path, wrap_response=wrap_response)
