import pymongo
from pymongo import MongoClient
from repository.abstract_repository import AbstractRepository
from util.logging_util import log_helper


class MongoRepository(AbstractRepository):
    mc = MongoClient("mongodb://localhost:27017")
    db = mc["banking"]
    collection = db["users"]
    logger = log_helper('INFO')

    @classmethod
    def get_document_id(cls, document_id):
        try:
            doc_id = cls.collection.find().sort(document_id, pymongo.DESCENDING).limit(1)[0][document_id]
        except BaseException as ex:
            doc_id = 1000
            cls.logger.info(ex)
        return doc_id

    @classmethod
    def get_record(cls, record_identifier, record_identifier_value):
        if record_identifier_value:
            data = cls.collection.find({record_identifier: record_identifier_value}, {"_id": 0})
        else:
            data = cls.collection.find({}, {"_id": 0})
        records = dict(data=[])
        for item in data:
            records["data"].append(item)
        return records

    @classmethod
    def delete_record(cls, record_identifier, record_identifier_value):
        response = cls.collection.delete_one({record_identifier: record_identifier_value})
        return str(response.deleted_count)

    @classmethod
    def add_record(cls, request_data, collection_name=None):
        _id = user_name = 0
        error_msg = None
        try:
            if collection_name:
                cls.collection = cls.db[collection_name]
            # request_data["user_name"] = cls.generate_user_name()
            doc = cls.collection.insert_one(request_data)
            _id, user_name = str(doc.inserted_id), request_data["username"]
        except BaseException as e:
            cls.logger.info(repr(e))
            error_msg = repr(e)
        return _id, user_name, error_msg

    @classmethod
    def update_record(cls, request_data):
        pass
