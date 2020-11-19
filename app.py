from flask import Flask, jsonify

from business.customer_service import Customer

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_customer_detail():
    customer = Customer('Test')
    return customer.get_customer_details('rrajeevan')


if __name__ == '__main__':
    app.run(debug=True)
