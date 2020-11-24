import abc


class AbstractRepository(abc.ABC):
    @classmethod
    def get_account_number(cls):
        raise NotImplementedError

    @classmethod
    def add_record(cls, request_data, collection_name):
        raise NotImplementedError

    @classmethod
    def update_record(cls, request_data):
        raise NotImplementedError

    @classmethod
    def get_record(cls, record_identifier, record_identifier_value):
        raise NotImplementedError

    @classmethod
    def delete_record(cls, request_data):
        raise NotImplementedError
