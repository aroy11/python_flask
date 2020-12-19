import pytest
from flask import Flask
from business import customer_service


class MockGetResponse:
    @staticmethod
    def values():
        return [{'UserName': 'jhonnyone', 'password': 'pbkdf2:sha256:150000$DBlDG8RX$b54055d6fefb40a2272c73ff7add04af9dcd332e880e3d4519848c37e754d0de', 'FirstName': 'John', 'accountNumber': 1001}]


class MockGetEmptyResponse:
    @staticmethod
    def values():
        return []


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
