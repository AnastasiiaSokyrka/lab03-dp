from abc import ABC, abstractmethod
from datetime import date


class DataType(ABC):
    @abstractmethod
    def validate(self, value):
        pass


class IntegerType(DataType):
    def validate(self, value):
        return value is None or (isinstance(value, int) and not isinstance(value, bool))


class StringType(DataType):
    def __init__(self, max_length=None):
        self.max_length = max_length

    def validate(self, value):
        if value is None:
            return True
        if not isinstance(value, str):
            return False
        return self.max_length is None or len(value) <= self.max_length


class BooleanType(DataType):
    def validate(self, value):
        return value is None or isinstance(value, bool)


class DateType(DataType):
    def validate(self, value):
        return value is None or (isinstance(value, date) and not isinstance(value, type(None)))
