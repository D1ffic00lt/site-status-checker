from checker.units.checker import Checker
from checker.units.exceptions import SSCException, IgnoreInternetExceptions
from checker.units.reader import CSVReader


class SiteStatusChecker(CSVReader):
    IGNORE_ERRORS: bool = False
    YIELD_ERRORS: bool = False

    def __init__(self, filename: str):
        self.data = super().__init__(filename)

    @staticmethod
    def error_checker(value):
        if issubclass(type(value), SSCException):
            return True
        return False

    @IgnoreInternetExceptions()
    def __call__(self):
        for reader in super().__call__():
            if self.error_checker(self.input_error_status):
                if not self.IGNORE_ERRORS:
                    yield str(self.input_error_status)
                    return
                if not self.YIELD_ERRORS:
                    yield str(self.input_error_status)
            worker = Checker(reader)()
            if self.error_checker(worker):
                if not self.IGNORE_ERRORS:
                    yield str(worker)
                    return
                if not self.YIELD_ERRORS:
                    yield str(worker)
                continue
            if worker is not None:
                yield worker

    def __str__(self):
        return "[{0}]".format(", ".join([str(obj) for obj in self.units]))

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)
