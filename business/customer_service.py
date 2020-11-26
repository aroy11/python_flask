from flask import make_response, jsonify, current_app
from repository.mongo_client import MongoRepository
from util.logging_util import log_helper
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

class Customer:
    def __init__(self, request_data):
        self.request_data = request_data
        self.mongo_repository = MongoRepository('mongodb://localhost:27017', 'banking', 'accounts')
        self.logger = log_helper('INFO')
        self.loan_collection = "loans"

    def login(self, auth):
        login_error_message = 'Could not verify'
        if not auth or not auth.get('username') or not auth.get('password'):
            return make_response(
                login_error_message,
                401,
                {'WWW-Authenticate': 'Login required'}
            )
        user = self.get_customer_details('username', auth.get('username'))
        if not user.get('data') == []:
            user_info = user.get('data')[0]
        else:
            user_info = None

        if not user_info:
            return make_response(
                login_error_message,
                403,
                {'WWW-Authenticate': 'Invalid credentials'}
            )

        if check_password_hash(user_info.get('password'), auth.get('password')):
            token = jwt.encode({
                'name': user_info.get('username'),
                'accountNumber': user_info.get('accountNumber'),
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, current_app.config['SECRET_KEY']).decode('ascii')

            return make_response(jsonify({'token': token}), 201)
        else:
            return make_response(
                login_error_message,
                403,
                {'WWW-Authenticate': 'Invalid credentials'}
            )

    def get_customer_details(self, search_condition, customer_identifier):
        self.logger.info('Inside get details method')
        try:
            if customer_identifier is None:
                return make_response(jsonify({"message": "Invalid search condition"}), 400)
            else:
                data = self.mongo_repository.get_record(search_condition, customer_identifier)
                if len(data) > 0:
                    # data["data"][0].pop("password")
                    return data
                return make_response(jsonify({"message": "No records found"}), 200)
        except Exception as e:
            self.logger.error(e)
            raise e

    def delete_customer(self, customer_id):
        self.logger.info('Inside delete customer details method')
        return self.mongo_repository.delete_record('accountNumber', customer_id)

    def delete_loan(self, loan_id):
        self.logger.info('Inside delete loan details method')
        return self.mongo_repository.delete_record('loanID', loan_id)

    def update_account_detail(self):
        self.logger.info('Updating account detail')
        return self.mongo_repository.update_record(self.request_data)

    def add_loan_details(self):
        self.logger.info('Inside add loan details method')
        try:
            data = self.request_data
            self.request_data["loanID"] = self.mongo_repository.get_document_number("loanID", self.loan_collection) + 1
            _id = self.mongo_repository.add_record(data, self.loan_collection)
            if _id:
                response = make_response(jsonify({"loanID": self.request_data["loanID"]}), 200)
                response.headers["trace_id"] = _id
            else:
                response = make_response(jsonify({"error": f"Error Adding loan data "}), 500)
        except Exception as ex:
            self.logger.error(repr(ex))
            response = make_response(jsonify({"Error": "Error Adding loan data"}), 500)
        return response

    def add_customer(self):
        self.logger.info('Inside add customer')
        _id = None
        acc_no: int = 0
        try:
            customer = self.get_customer_details("username", self.request_data["username"])
            if customer and customer.get('data') == []:
                self.request_data["accountNumber"] = self.mongo_repository.get_document_number("accountNumber") + 1
                self.request_data["password"] = generate_password_hash(self.request_data["password"])
                _id = self.mongo_repository.add_record(self.request_data)
                if _id:
                    acc_no = self.request_data["accountNumber"]
                    response = make_response(jsonify({"accountNumber": acc_no}), 200)
                    response.headers["trace_id"] = _id
                else:
                    response = make_response(jsonify({"Warning": "Could not create customer"}), 201)
            else:
                response = make_response('User already exists. Please Log in', 202)
        except Exception as ex:
            self.logger.error(repr(ex))
            response = make_response(jsonify({"Error": "Error occurred on customer creation"}), 500)
        return response

    def get_loan_details(self):
        self.logger.info('Inside get loan details')
        try:
            loan_data = self.mongo_repository.get_record("loanID", int(self.request_data), self.loan_collection)
            if loan_data and len(loan_data["data"]) > 0:
                response = make_response(loan_data, 200)
            else:
                response = make_response(jsonify({"Info": "Loan details not found"}), 201)
        except Exception as ex:
            self.logger.error(repr(ex))
            response = make_response(jsonify({"Error": "Error occurred while fetching loan details"}), 500)
        return response
