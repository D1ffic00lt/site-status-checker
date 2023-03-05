from typing import Union, List
from checker.units.reader import CSVReader
from checker.units.checker import Checker
from checker.units.exceptions import SSCException


class SiteStatusChecker(object):
    IGNORE_ERRORS: bool = False

    def __init__(self, data: CSVReader):
        self._data: List[Union[CSVReader]] = [data]

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
            if self.error_checker(reader.input_error_status) and not self.IGNORE_ERRORS:
                yield str(reader.input_error_status)
                return
            for read_object in reader():
                worker = Checker(read_object)()
                if self.error_checker(worker):
                    yield worker
                    if not self.IGNORE_ERRORS:
                        return
                if worker is not None:
                    yield worker

    def __str__(self):
        return "[{0}]".format(", ".join([str(obj) for obj in self._data]))

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

