import json
from bson import json_util
from flask import jsonify

from pymongo import MongoClient

from repository.abstract_repository import AbstractRepository
from util.logging_util import log_helper


class MongoRepository(AbstractRepository):
    mc = MongoClient("mongodb://localhost:27017")
    db = mc["banking"]
    coll = db["users"]
    logger = log_helper('INFO')

    @classmethod
    def get_record(cls, record_identifier, record_identifier_value):
        response = cls.collection.find_one({record_identifier: record_identifier_value})
        cls.logger.info(response)
        return json.loads(json_util.dumps(response))

    @classmethod
    def delete_record(cls, request_data):
        pass

    @classmethod
    def update_record(cls, request_data):
        account = cls.collection.find_one({'_id': request_data.record_identifier_value})
        if not account:
            return jsonify({"error": "Login failed"}), 401

        x = cls.collection.update_one({'_id': request_data.record_identifier_value}, request_data)
        return x.upserted_id

    @classmethod
    def add_record(cls, request_data=None, collection_name=None):
        _id = user_name = 0
        error_msg = None
        try:
            if collection_name:
                cls.coll = cls.db["loan"]
            # request_data["user_name"] = cls.generate_user_name()
            doc = cls.coll.insert_one(request_data)
            _id, user_name = str(doc.inserted_id), request_data["username"]
        except BaseException as e:
            cls.logger.info(repr(e))
            error_msg = repr(e)
        return _id, user_name, error_msg

