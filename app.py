from flask import Flask, jsonify, request

from business.customer_service import Customer

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_customer_detail():
    customer = Customer('Test')
    return customer.get_customer_details('rrajeevan')


@app.route('/update', methods=['POST'])
def update_account_detail():
    data = request.json
    customer = Customer('Test')
    return customer.update_account_detail(data)


if __name__ == '__main__':
    app.run(debug=True)
