import json
import pytest


from app import app


@pytest.fixture(scope='module')
def test_client():
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def test_token(test_client):
    login_response = test_client.post('/login', json={'username': 'johndoe1234', 'password': 'Blue123456'})
    token = json.loads(login_response.data)['token']
    return token

@pytest.fixture(scope='module')
def add_customer(test_client):
    data = { "username": "johndoe2", "password": "Blue123", "name": "John Doe", "accountType": "savings", "address": "1 Main Street", "state": "Test", "pan": "aaaaa5678a", "contactNo": "1234567890", "dob": "10-18-2020", "country": "India", "emailAddress": "test@tt.co"}
    response = test_client.post('/register', json=data)
    return response.json['accountNumber']