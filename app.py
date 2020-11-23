from flask import Flask, jsonify, request, make_response
from flask_bcrypt import Bcrypt
import jwt
from business.customer_service import Customer
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'   # TO DO - read from config file

@app.route('/', methods=['GET'])
def get_customer_detail():
    customer = Customer('Test')
    return customer.get_customer_details('rrajeevan')


@app.route('/update', methods=['POST'])
def update_account_detail():
    data = request.json
    customer = Customer('Test')
    return customer.update_account_detail(data)


@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    bcrypt = Bcrypt()
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Login required'}
        )
    customer = Customer('Test')
    user = customer.get_customer_details(auth.get('username'))
    if not user:
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Invalid credentials'}
        )

    if bcrypt.check_password_hash(user.get('password'), auth.get('password')):
        token = jwt.encode({
            'name': user.get('userName'),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    else:
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Invalid credentials'}
    )

if __name__ == '__main__':
    app.run(debug=True)
