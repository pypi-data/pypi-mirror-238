from .mongo_resource import MongoResource
from .general import generate_project_name


class ProjectResource(MongoResource):
    def __init__(
        self, namespace, app_id, boundary_id, requestor, collection_name, request_data
    ):
        super().__init__(app_id, collection_name)
        self.namespace = namespace
        self.boundary_id = boundary_id
        self.project_name = generate_project_name(self.app_id, self.boundary_id)
        self.requestor = requestor
        self.request_data = request_data
