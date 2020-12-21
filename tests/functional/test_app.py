import json


def test_customer_login_success(test_client):
    response = test_client.post('/login', json={'username': 'johndoe', 'password': 'Welcome'})
    assert response.status_code == 201


def test_customer_login_invalid_user_detail(test_client):
    response = test_client.post('/login', json={'username1': 'test01', 'password': 'Test0101'})
    assert response.status_code == 401


def test_customer_get_details_success(test_client, test_token):
    url_path = '/customer?accountNumber=1004'
    get_response = test_client.get(url_path, headers={'Authorization': test_token})
    assert get_response.status_code == 200


def test_customer_get_details_missing_identifier(test_client, test_token):
    url_path = '/customer'
    get_response = test_client.get(url_path, headers={'Authorization': test_token})
    assert get_response.status_code == 404


def test_customer_get_details_no_record_in_db(test_client, test_token):
    url_path = '/customer?accountNumber=800'
    get_response = test_client.get(url_path, headers={'Authorization': test_token})
    assert get_response.status_code == 200
    assert json.loads(get_response.data)['message'] == 'No records found'

def test_customer_delete_customer_success(test_client, test_token, add_customer):
    url_path = f'/customer'
    data = { "accountNumber": f"{add_customer}"}
    delete_response = test_client.delete(url_path, headers={'Authorization': test_token}, json=data)
    assert delete_response.status_code == 200
    assert delete_response.data == b'Deleted'

def test_get_loan_details_success(test_client, test_token):
    url_path = '/loan?loanID=1001'
    get_response = test_client.get(url_path, headers={'Authorization': test_token})
    assert get_response.status_code == 200


def test_get_loan_details_missing_identifier(test_client, test_token):
    url_path = '/loan'
    get_response = test_client.get(url_path, headers={'Authorization': test_token})
    assert get_response.status_code == 404


def test_get_loan_details_no_record_found(test_client, test_token):
    url_path = '/loan?loanID=2020'
    get_response = test_client.get(url_path, headers={'Authorization': test_token})
    assert get_response.status_code == 200
    assert json.loads(get_response.data)['message'] == 'No records found'
