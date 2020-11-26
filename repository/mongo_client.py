import pymongo
from pymongo import MongoClient
from repository.abstract_repository import AbstractRepository
from util.logging_util import log_helper


class MongoRepository(AbstractRepository):
    def __init__(self, host_uri, database_name, collection_name):
        self.client = MongoClient(host_uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.logger = log_helper('INFO')

    def get_document_number(self, document_id, collection_name=None):
        try:
            if collection_name:
                self.collection = self.db[collection_name]
            doc_id = self.collection.find().sort(document_id, pymongo.DESCENDING).limit(1)[0][document_id]
        except BaseException as ex:
            doc_id = 1000
            self.logger.info(ex)
        return doc_id

    def get_record(self, record_identifier, record_identifier_value=None, collection_name=None):
        if collection_name:
            self.collection = self.db[collection_name]
        if record_identifier_value:
            data = self.collection.find({record_identifier: record_identifier_value}, {"_id": 0})
        else:
            data = self.collection.find({}, {"_id": 0})
        records = dict(data=[])
        for item in data:
            records["data"].append(item)
        return records

    def delete_record(self, record_identifier, record_identifier_value=None, collection_name=None):
        response = self.collection.delete_one({record_identifier: record_identifier_value})
        return str(response.deleted_count)

    def add_record(self, request_data, collection_name=None):
        if collection_name:
            self.collection = self.db[collection_name]
        response = self.collection.insert_one(request_data)
        self.logger.info(response.inserted_id)
        return response.inserted_id

    def update_record(self, data_for_update, query=None, collection_name=None):
        if collection_name:
            self.collection = self.db[collection_name]
        if query is None:
            response = self.collection.update_many({}, {"$set": data_for_update})
        else:
            response = self.collection.update_one(query, {"$set": data_for_update})
        return response
