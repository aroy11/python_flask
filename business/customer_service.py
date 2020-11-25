from flask import make_response, jsonify
from repository.mongo_client import MongoRepository
from util.logging_util import log_helper
from werkzeug.security import generate_password_hash


class Customer:
    logger = log_helper('INFO')

    @classmethod
    def get_customer_details(cls, customer_id):
        cls.logger.info('Inside get details method')
        return MongoRepository.get_record('userName', customer_id)

    @classmethod
    def delete_customer(cls, customer_id):
        cls.logger.info('Inside delete details method')
        return MongoRepository.delete_record('userName', customer_id)

    @classmethod
    def update_account_detail(cls, request_data):
        cls.logger.info('Updating account detail')
        return MongoRepository.update_record(request_data)

    @classmethod
    def add_loan_details(cls, request_data):
        cls.logger.info('Inside add loan details method')
        _id, user_name, error_msg = MongoRepository.add_record(request_data, "loan")
        if error_msg:
            response = make_response(jsonify({"error": f"Error Adding Customer data - {error_msg}"}), 500)
        else:
            response = make_response(jsonify({"username": user_name}), 200)
            response.headers["trace_id"] = _id
        return response

    @classmethod
    def add_customer(cls, request_data):
        cls.logger.info('Inside add customer')
        _id = None
        acc_no: int = 0
        try:
            request_data["accountNumber"] = MongoRepository.get_account_number() + 1
            request_data["password"] = generate_password_hash(request_data["password"])
            _id = MongoRepository.add_record(request_data)
            if _id:
                acc_no = request_data["accountNumber"]
                response = make_response(jsonify({"accountNumber": acc_no}), 200)
                response.headers["trace_id"] = _id
            else:
                response = make_response(jsonify({"Warning": "Could not create customer"}), 201)
        except BaseException as ex:
            cls.logger.error(repr(ex))
            response = make_response(jsonify({"Error": "Error occurred on customer creation"}), 500)
        return response

    @classmethod
    def get_loan_details(cls, request_data):
        cls.logger.info('Inside get loan details')
        try:
            loan_data = MongoRepository.get_record("LoanId", int(request_data))
            if loan_data and len(loan_data["data"]) > 0:
                response = make_response(loan_data, 200)
            else:
                response = make_response(jsonify({"Info": "Loan details not found"}), 201)
        except BaseException as ex:
            cls.logger.error(repr(ex))
            response = make_response(jsonify({"Error": "Error occurred while fetching loan details"}), 500)
        return response
