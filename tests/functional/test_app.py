import json


def test_customer_login_invalid_user_detail(test_client):
    response = test_client.post('/login', json={ 'username1' :'test01','password': 'Test0101'})
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
