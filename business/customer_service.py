from flask import make_response, jsonify

from repository.mongo_client import MongoRepository
from util.logging_util import log_helper


class Customer:
    logger = log_helper('INFO')

    @classmethod
    def get_customer_details(cls, customer_id):
        cls.logger.info('Inside get details method')
        return cls.db_client.get_record('userName', customer_id)

    @classmethod
    def update_account_detail(cls, account_data):
        cls.logger.info('Updating account detail')
        return cls.db_client.update_record(account_data)

    @classmethod
    def add_loan_details(cls, request_data):
        cls.logger.info('Inside add loan details method')
        data = request_data.json
        _id, user_name, error_msg = MongoRepository.add_record(data)
        if error_msg:
            response = make_response(jsonify({"error": f"Error Adding Customer data - {error_msg}"}), 500)
        else:
            response = make_response(jsonify({"username": user_name}), 200)
            response.headers["trace_id"] = _id
        return response
