from repository.mongo_client import MongoRepository
from util.logging_util import log_helper


class Customer:
    def __init__(self, request_data):
        self.request_data = request_data
        self.db_client = MongoRepository('mongodb://localhost:27017/', 'banking', 'accounts')
        self.logger = log_helper('INFO')

    def get_customer_details(self, customer_id):
        self.logger.info('Inside get details method')
        return self.db_client.get_record('userName', customer_id)
