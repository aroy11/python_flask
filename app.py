from flask import Flask, jsonify, request, make_response
from flask_jsonschema_validator import JSONSchemaValidator
from jsonschema import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from business.customer_service import Customer

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'  # TO DO - read from config file
JSONSchemaValidator(app=app, root="schemas")  # folder


@app.errorhandler(ValidationError)
def on_validation_error(e):
    return make_response(jsonify({"error": str(e)}), 400)


@app.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer_detail(customer_id):
    customer = Customer(customer_id)
    return customer.get_customer_details('accountNumber', customer_id)


@app.route('/register', methods=["POST"])
def register_customer():
    data = request.json
    customer = Customer(data)
    return customer.add_customer()


@app.route('/loan/<loan_id>', methods=["GET"])
def loan_detail(loan_id):
    customer = Customer(loan_id)
    return customer.get_loan_details()


@app.route('/customer', methods=['POST'])
def update_account_detail():
    data = request.json
    customer = Customer(data)
    return customer.update_account_detail()


@app.route('/customer/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    delete_response = Customer.delete_customer(customer_id)
    if int(delete_response) == 0:
        return make_response('Could not delete: User not found', 404)
    elif int(delete_response):
        return make_response('Deleted', 200)


@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Login required'}
        )
    customer = Customer(auth)
    user = customer.get_customer_details('username', auth.get('username'))
    if not user.get('data') == []:
        userInfo = user.get('data')[0]
    else:
        userInfo = None

    if not userInfo:
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Invalid credentials'}
        )

    if check_password_hash(userInfo.get('password'), auth.get('password')):
        token = jwt.encode({
            'name': userInfo.get('username'),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token}), 201)
    else:
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Invalid credentials'}
        )


@app.route('/loan', methods=['POST'])
@app.validate('loan', 'add')  # file name, schema name
def add_loan_details():
    data = request.json
    customer = Customer(data)
    return customer.add_loan_details()


if __name__ == '__main__':
    app.run(debug=True)