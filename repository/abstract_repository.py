import abc


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_record(self, request_data, table_name):
        raise NotImplementedError

    @abc.abstractmethod
    def update_record(self, request_data, table_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_record(self, record_identifier, record_identifier_value):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_record(self, request_data):
        raise NotImplementedError
