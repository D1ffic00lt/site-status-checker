from checker.units.exceptions import SSCException
from checker.units.reader import CSVReader
from checker.units.converter import Converter


class SiteStatusChecker(CSVReader):
    IGNORE_ERRORS: bool = False
    YIELD_ERRORS: bool = False

    def __init__(self, filename: str):
        self.data = super().__init__(filename)

    @staticmethod
    def error_checker(value):
        if isinstance(value, SSCException):
            return True
        return False

    def __call__(self):
        for reader in super().__call__():
            if self.error_checker(self.input_error_status) and not self.IGNORE_ERRORS:
                yield str(self.input_error_status)
                return
            else:
                worker = Converter(reader)
                if self.error_checker(worker):
                    if self.YIELD_ERRORS and self.IGNORE_ERRORS:
                        yield worker.get_text_description()
                    if not self.IGNORE_ERRORS:
                        yield worker.get_text_description()
                        return
                    continue
                if worker is not None:
                    yield worker.get_text_description()

    def __str__(self):
        return "[{0}]".format(", ".join([str(obj) for obj in self.units]))

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)
