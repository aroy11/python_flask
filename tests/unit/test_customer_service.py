import pytest
from flask import Flask

from business import customer_service


class MockGetResponse:
    @staticmethod
    def values():
        return [{'UserName': 'jhonnyone',
                 'password': 'pbkdf2:sha256:150000$DBlDG8RX$b54055d6fefb40a2272c73ff7add04af9dcd332e880e3d4519848c37e754d0de',
                 'FirstName': 'John', 'accountNumber': 1001}]

    @staticmethod
    def get(data):
        return []


class MockGetCustomerResponse:
    @staticmethod
    def get(data):
        return [{'UserName': 'jhonnytwo',
                 'password': 'pbkdf2:sha256:150000$aVIJU0sw$edd225a7253f4e98f29a635cb0fff37aa23379a4a570471588c3cbedc0cd5ecf',
                 'FirstName': 'Ben', 'accountNumber': 1002}]


class MockGetEmptyCustomerResponse:
    @staticmethod
    def get(data):
        return []


class MockGetEmptyResponse:
    @staticmethod
    def values():
        return []


class MockGetLoanResponse:
    def __init__(self):
        self.data = [{'username': 'ken45',
                 'loanID': 1001,
                 'loanType': 'VL', 'loanAmount': 20000}]

    @staticmethod
    def values():
        return [{'username': 'ken45',
                 'loanID': 1001,
                 'loanType': 'VL', 'loanAmount': 20000}]


class MockMongoInsertResponse:
    @staticmethod
    def values():
        return [{'_id': '5fbf32ee732167b2ad6c7666'}]


class TestCustomerService:

    @pytest.fixture
    def return_valid_response(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockGetResponse()

        def mock_add(*args, **kwargs):
            return MockMongoInsertResponse()

        def mock_get_doc_number(*args, **kwargs):
            return 1000

        customer = customer_service.Customer(1001)
        monkeypatch.setattr(customer.mongo_repository, "get_record", mock_get)
        monkeypatch.setattr(customer.mongo_repository, "get_document_number", mock_get_doc_number)
        monkeypatch.setattr(customer.mongo_repository, "add_record", mock_add)
        return customer

    @pytest.fixture
    def return_empty_response(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockGetEmptyResponse()

        customer = customer_service.Customer(1001)
        monkeypatch.setattr(customer.mongo_repository, "get_record", mock_get)
        return customer

    @pytest.fixture
    def return_valid_response_login(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockGetCustomerResponse()

        customer = customer_service.Customer({"username": "test", "password": "Welcome"})
        monkeypatch.setattr(customer, "get_customer_details", mock_get)
        return customer

    @pytest.fixture
    def invalid_username_login(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockGetEmptyCustomerResponse()

        customer = customer_service.Customer({"username": "test", "password": "testpassword"})
        monkeypatch.setattr(customer, "get_customer_details", mock_get)
        return customer

    @pytest.fixture
    def invalid_password_login(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockGetCustomerResponse()

        customer = customer_service.Customer({"username": "test", "password": "wrongpassword"})
        monkeypatch.setattr(customer, "get_customer_details", mock_get)
        return customer

    @pytest.fixture
    def return_valid_loan_response(self, monkeypatch):
        def mock_get(*args, **kwargs):
            #return MockGetLoanResponse()
            return {"data": [{'username': 'ken45',
                 'loanID': 1001,
                 'loanType': 'VL', 'loanAmount': 20000}]}

        customer = customer_service.Customer(1001)
        monkeypatch.setattr(customer.mongo_repository, "get_record", mock_get)
        return customer

    @pytest.fixture
    def return_empty_response_loan(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return {"data": []}

        customer = customer_service.Customer(1001)
        monkeypatch.setattr(customer.mongo_repository, "get_record", mock_get)
        return customer

    def test_add_customer(self, return_valid_response):
        app = Flask(__name__)
        with app.app_context():
            customer = return_valid_response.get_customer_details('username', 'testuser')
            if customer and customer.get('data') == []:
                return_valid_response.request_data = {
                    "username": "testuser",
                    "password": "Blue1234",
                    "name": "John Doe",
                    "accountType": "savings",
                    "address": "1 Main Street",
                    "state": "Test",
                    "pan": "aaaaa5678a",
                    "contactNo": "9037843092",
                    "dob": "10-18-2020",
                    "country": "India",
                    "emailAddress": "test@tt.co"
                }
                _id = return_valid_response.add_customer()

    def test_get_customer_details_success_account_number(self, return_valid_response):
        response = return_valid_response.get_customer_details('accountNumber', 1001)
        assert response is not None

    def test_get_customer_details_without_results(self, return_empty_response):
        app = Flask(__name__)
        with app.app_context():
            response = return_empty_response.get_customer_details('accountNumber', 1001, True)
            assert response.json['message'] == 'No records found'

    def test_get_customer_details_without_results_without_message(self, return_empty_response):
        response = return_empty_response.get_customer_details('accountNumber', 1001)
        assert response is not None

    def test_get_customer_details_without_identifier(self):
        app = Flask(__name__)
        with app.app_context():
            customer = customer_service.Customer(1001)
            response = customer.get_customer_details('accountNumber', None, True)
            assert response.json['message'] == 'Invalid search condition'

    def test_get_loan_details_success_account_number(self, return_valid_loan_response):
        app = Flask(__name__)
        with app.app_context():
            response = return_valid_loan_response.get_loan_details(1001)
            assert response is not None

    def test_get_loan_details_without_results(self, return_empty_response_loan):
        app = Flask(__name__)
        with app.app_context():
            response = return_empty_response_loan.get_loan_details(2020)
            assert response.json['Info'] == 'Loan details not found'

    def test_login_valid_credentials_should_return_valid_jwt_token(self, return_valid_response_login):
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test'
        with app.app_context():
            response = return_valid_response_login.login()
            assert response.json['token'] is not None
            assert response.status_code == 201

    def test_login_invalid_username_should_return_error(self, invalid_username_login):
        app = Flask(__name__)
        with app.app_context():
            response = invalid_username_login.login()
            assert response.headers['WWW-Authenticate'] == 'Invalid credentials'
            assert response.status_code == 403

    def test_login_invalid_password_should_return_error(self, invalid_password_login):
        app = Flask(__name__)
        with app.app_context():
            response = invalid_password_login.login()
            assert response.headers['WWW-Authenticate'] == 'Invalid credentials'
            assert response.status_code == 403
