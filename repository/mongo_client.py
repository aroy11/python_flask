import json
from bson import json_util

from pymongo import MongoClient

from repository.abstract_repository import AbstractRepository
from util.logging_util import log_helper


class MongoRepository(AbstractRepository):

    def __init__(self, host_uri, database_name, collection_name):
        self.client = MongoClient(host_uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.logger = log_helper('INFO')

    def get_record(self, record_identifier, record_identifier_value):
        response = self.collection.find_one({record_identifier: record_identifier_value})
        self.logger.info(response)
        return json.loads(json_util.dumps(response))

    def delete_record(self, request_data):
        pass

    def update_record(self, request_data):
        pass

    def add_record(self, request_data):
        pass
