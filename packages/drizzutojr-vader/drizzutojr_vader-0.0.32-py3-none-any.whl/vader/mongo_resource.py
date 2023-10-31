import datetime

from abc import ABC, abstractmethod

from .mongo import connect
from .exceptions import VaderMongoError


class MongoResource(ABC):
    def __init__(self, app_id, collection_name):
        self.app_id = app_id
        self.collection_name = collection_name

        self.mongo_connection = None

    def _create_mongo_connection(self):
        self._create_mongo_filter()
        if self.mongo_connection == None:
            self.mongo_connection = connect()

    def _get_mongo_collection(self):
        self._create_mongo_connection()
        return self.mongo_connection[self.collection_name]

    def _save_document_to_collection(self, document):
        self._create_mongo_connection()
        timestamp = datetime.datetime.now()
        document["metadata"]["last_updated"] = str(timestamp)
        document["metadata"]["last_updated_by"] = self.requestor

        if not document["metadata"]["created_on"]:
            document["metadata"]["created_on"] = str(timestamp)

        try:
            self._get_mongo_collection().replace_one(self.mongo_filter, document, True)
        except Exception as e:
            raise VaderMongoError(
                f"Error with saving document {document['_id']} in collection {self.collection_name}: {str(e)}"
            )

    def _get_document_from_collection(self):
        self._create_mongo_connection()
        return self._get_mongo_collection().find_one(self.mongo_filter)

    @abstractmethod
    def _delete_document_from_collection(self):
        raise NotImplementedError

    @abstractmethod
    def _create_mongo_filter(self):
        raise NotImplementedError

    @abstractmethod
    def _create_new_config(self):
        raise NotImplementedError
