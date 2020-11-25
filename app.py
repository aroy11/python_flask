from flask import Flask, jsonify, request, make_response
import jwt
from flask_jsonschema_validator import JSONSchemaValidator
from jsonschema import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from business.customer_service import Customer
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'  # TO DO - read from config file
JSONSchemaValidator(app=app, root="schemas")  # folder


@app.errorhandler(ValidationError)
def on_validation_error(e):
    # return Response("There was a validation error: " + str(e), 400)
    return make_response(jsonify({"error": str(e)}), 400)


@app.route('/', methods=['GET'])
def get_customer_detail():
    return Customer.get_customer_details('rrajeevan')


@app.route('/register', methods=["POST"])
def register_customer():
    data = request.json
    return Customer.add_customer(data)


@app.route('/loan/<loan_id>', methods=["GET"])
def loan_detail(loan_id):
    # loan_id = request.args.get("loan_id", None)
    return Customer.get_loan_details()


@app.route('/update', methods=['POST'])
def update_account_detail():
    data = request.json
    return Customer.update_account_detail(data)

@app.route('/delete/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    delete_response = Customer.delete_customer(customer_id)
    if int(delete_response) == 0:
        return make_response('Could not delete: User not found', 404)
    elif int(delete_response):
        return make_response('Deleted', 200)

@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Login required'}
        )

    user = Customer.get_customer_details(auth.get('username'))
    userInfo = user.get('data')[0]

    if not userInfo:
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Invalid credentials'}
        )

    if check_password_hash(userInfo.get('password'), auth.get('password')):
        token = jwt.encode({
            'name': userInfo.get('userName'),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
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
    return Customer.add_loan_details(data)


if __name__ == '__main__':
    app.run(debug=True)
