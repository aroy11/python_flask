from flask import make_response, jsonify
from repository.mongo_client import MongoRepository
from util.logging_util import log_helper
from werkzeug.security import generate_password_hash


class Customer:
    def __init__(self, request_data):
        self.request_data = request_data
        self.mongo_repository = MongoRepository('mongodb://localhost:27017', 'banking', 'accounts')
        self.logger = log_helper('INFO')

    def update_account_detail(self):
        self.logger.info('Updating account detail')
        return self.mongo_repository.update_record(self.request_data)

    def add_loan_details(self):
        self.logger.info('Inside add loan details method')
        data = self.request_data
        _id, user_name, error_msg = self.mongo_repository.add_record(data)
        if error_msg:
            response = make_response(jsonify({"error": f"Error Adding Customer data - {error_msg}"}), 500)
        else:
            response = make_response(jsonify({"username": user_name}), 200)
            response.headers["trace_id"] = _id
        return response

    def add_customer(self):
        self.logger.info('Inside add customer')
        _id = None
        acc_no: int = 0
        try:
            self.request_data["AccountNumber"] = self.mongo_repository.get_account_number() + 1
            self.request_data["Password"] = generate_password_hash(self.request_data["Password"])
            _id = self.mongo_repository.add_record(self.request_data)
            if _id:
                acc_no = self.request_data["AccountNumber"]
                response = make_response(jsonify({"AccountNumber": acc_no}), 200)
                response.headers["trace_id"] = _id
            else:
                response = make_response(jsonify({"Warning": "Could not create customer"}), 201)
        except BaseException as ex:
            self.logger.error(repr(ex))
            response = make_response(jsonify({"Error": "Error occurred on customer creation"}), 500)
        return response

    def get_loan_details(self):
        self.logger.info('Inside get loan details')
        try:
            loan_data = self.mongo_repository.get_record("LoanId", self.request_data)
            if loan_data and len(loan_data["data"]) > 0:
                response = make_response(loan_data, 200)
            else:
                response = make_response(jsonify({"Info": "Loan details not found"}), 201)
        except BaseException as ex:
            self.logger.error(repr(ex))
            response = make_response(jsonify({"Error": "Error occurred while fetching loan details"}), 500)
        return response
