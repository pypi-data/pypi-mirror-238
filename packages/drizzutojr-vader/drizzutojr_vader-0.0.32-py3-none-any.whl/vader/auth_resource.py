from .project_resource import ProjectResource
from .exceptions import VaderConfigError


class AuthResource(ProjectResource):
    def __init__(
        self, namespace, app_id, boundary_id, requestor, collection_name, request_data
    ):
        if "identity_id" not in request_data:
            raise VaderConfigError(f"Request Data missing required identity_id")
        self.identity_id = request_data["identity_id"]
        super().__init__(
            namespace, app_id, boundary_id, requestor, collection_name, request_data
        )
