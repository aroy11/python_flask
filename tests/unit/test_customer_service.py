import pytest
from flask import Flask
from business import customer_service


class MockGetResponse:
    @staticmethod
    def values():
        return [{'UserName': 'jhonnyone',
                 'password': 'pbkdf2:sha256:150000$DBlDG8RX$b54055d6fefb40a2272c73ff7add04af9dcd332e880e3d4519848c37e754d0de',
                 'FirstName': 'John', 'accountNumber': 1001}]


class MockGetEmptyResponse:
    @staticmethod
    def values():
        return []


class MockGetLoanResponse:
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

        customer = customer_service.Customer(1001)
        monkeypatch.setattr(customer.mongo_repository, "get_record", mock_get)
        return customer

    @pytest.fixture
    def return_empty_response(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockGetEmptyResponse()

        customer = customer_service.Customer(1001)
        monkeypatch.setattr(customer.mongo_repository, "get_record", mock_get)
        return customer

    @pytest.fixture
    def return_valid_loan_response(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockGetLoanResponse()

        customer = customer_service.Customer(1001)
        monkeypatch.setattr(customer.mongo_repository, "get_record", mock_get)
        return customer


    @pytest.fixture
    def return_valid_accountnumber_response(self, monkeypatch):
        customer = customer_service.Customer()
        monkeypatch.setattr(customer.mongo_repository, "get_document_number")
        return 1000

    @pytest.fixture
    def return_valid_addcustomer_response(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockMongoInsertResponse()

        customer = customer_service.Customer()
        monkeypatch.setattr(customer.mongo_repository, "add_record", mock_get)
        return customer

    def test_add_customer(self):
        customer = self.return_valid_response.get_customer_details('username', self.request_data["username"])
        if customer and customer.get('data') == []:
            self.request_data["accountNumber"] = self.return_valid_accountnumber_response.get_document_number(
                'accountNumber')
            self.request_data["password"] = generate_password_hash(self.request_data["password"])
            _id = self.return_valid_addcustomer_response.add_record(self.request_data)

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
        response = return_valid_loan_response.get_loan_details('loanID', 1001)
        assert response is not None

    def test_get_loan_details_without_results(self, return_empty_response):
        app = Flask(__name__)
        with app.app_context():
            response = return_empty_response.get_loan_details('loanID', 1005, True)
            assert response.json['message'] == 'No records found'

    def test_get_loan_details_without_results_without_message(self, return_empty_response):
        response = return_empty_response.get_loan_details('loanID', 1001)
        assert response is not None
