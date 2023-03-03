from typing import Union, List
from units.reader import CSVReader
from units.checker import Checker
from units.exceptions import SSCException


class SiteStatusChecker(object):
    def __init__(self, data: Union[CSVReader, None] = None):
        self._data: List[Union[CSVReader, None]] = [data]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: CSVReader):
        self._data.append(value)

    @staticmethod
    def error_checker(value):
        if issubclass(type(value), SSCException):
            return True
        return False

    def __call__(self):
        for reader in self.data:
            if reader.input_error_status:
                return "bad"
            for read_object in reader():
                worker = Checker(read_object)()
                if self.error_checker(worker):
                    return worker  # TODO
                yield worker

    def __str__(self):
        return "[{0}]".format(", ".join([str(obj) for obj in self._data]))

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)
