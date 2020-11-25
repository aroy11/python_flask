from flask import make_response, jsonify
from repository.mongo_client import MongoRepository
from util.logging_util import log_helper
from werkzeug.security import generate_password_hash


class Customer:
    def __init__(self, request_data):
        self.request_data = request_data
        self.mongo_repository = MongoRepository('mongodb://localhost:27017', 'banking', 'accounts')
        self.logger = log_helper('INFO')

    def get_customer_details(self, search_condition, customer_identifier):
        self.logger.info('Inside get details method')
        try:
            if customer_identifier is None:
                return make_response(jsonify({"message": "Invalid search condition"}), 400)
            else:
                data = self.mongo_repository.get_record(search_condition, customer_identifier)
                if len(data) > 0:
                    #data["data"][0].pop("password")
                    return data
                return make_response(jsonify({"message": "No records found"}), 200)
        except Exception as e:
            self.logger.error(e)
            raise e


    def delete_customer(self, customer_id):
        self.logger.info('Inside delete details method')
        return self.mongo_repository.delete_record('userName', customer_id)

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
            self.request_data["accountNumber"] = self.mongo_repository.get_account_number() + 1
            self.request_data["password"] = generate_password_hash(self.request_data["password"])
            _id = self.mongo_repository.add_record(self.request_data)
            if _id:
                acc_no = self.request_data["accountNumber"]
                response = make_response(jsonify({"accountNumber": acc_no}), 200)
                response.headers["trace_id"] = _id
            else:
                response = make_response(jsonify({"Warning": "Could not create customer"}), 201)
        except Exception as ex:
            self.logger.error(repr(ex))
            response = make_response(jsonify({"Error": "Error occurred on customer creation"}), 500)
        return response

    def get_loan_details(self):
        self.logger.info('Inside get loan details')
        try:
            loan_data = self.mongo_repository.get_record("loanId", int(self.request_data))
            if loan_data and len(loan_data["data"]) > 0:
                response = make_response(loan_data, 200)
            else:
                response = make_response(jsonify({"Info": "Loan details not found"}), 201)
        except Exception as ex:
            self.logger.error(repr(ex))
            response = make_response(jsonify({"Error": "Error occurred while fetching loan details"}), 500)
        return response
