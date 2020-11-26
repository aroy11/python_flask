from flask import Flask, jsonify, request, make_response
from flask_jsonschema_validator import JSONSchemaValidator
from jsonschema import ValidationError
import jwt

from business.customer_service import Customer

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'  # TO DO - read from config file
JSONSchemaValidator(app=app, root="schemas")  # folder


@app.errorhandler(ValidationError)
def on_validation_error(e):
    return make_response(jsonify({"error": str(e)}), 400)


def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({
                'message': 'Token is missing.'
            }), 401

        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({
                'message': 'Token is invalid.'
            }), 401
        return f(*args, **kwargs)

    decorated.__name__ = f.__name__
    return decorated


@app.route('/register', methods=["POST"])
@app.validate('customer', 'add')  # file name, schema name
def register_customer():
    data = request.json
    customer = Customer(data)
    return customer.add_customer()


@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    customer = Customer(auth)
    return customer.login()


@app.route('/customer', methods=['POST'])
@token_required
def update_account_detail():
    data = request.json
    customer = Customer(data)
    return customer.update_account_detail()


@app.route('/customer/<int:customer_id>', methods=['GET'])
@token_required
def get_customer_detail(customer_id):
    customer = Customer(customer_id)
    return customer.get_customer_details('accountNumber', customer_id)


@app.route('/customer', methods=['DELETE'])
@token_required
def delete_customer():
    data = request.json
    customer = Customer(data)
    delete_response = customer.delete_customer()
    if int(delete_response) == 0:
        return make_response('Could not delete: User not found', 404)
    elif int(delete_response):
        return make_response('Deleted', 200)


@app.route('/loan', methods=['POST'])
@app.validate('loan', 'add')  # file name, schema name
@token_required
def add_loan_details():
    data = request.json
    customer = Customer(data)
    return customer.add_loan_details()


@app.route('/loan', methods=["GET"])
@token_required
def loan_detail():
    data = request.json
    customer = Customer(data)
    return customer.get_loan_details()


@app.route('/loan', methods=['DELETE'])
@token_required
def delete_loan():
    data = request.json
    customer = Customer(data)
    delete_response = customer.delete_loan()
    if int(delete_response) == 0:
        return make_response('Could not delete: Loan details not found', 404)
    elif int(delete_response):
        return make_response('Deleted', 200)


if __name__ == '__main__':
    app.run(debug=True)
