from checker.units.controller import Controller
from checker.units.exceptions import SSCException
from checker.units.reader import CSVReader

class SiteStatusChecker(CSVReader):
    IGNORE_ERRORS: bool = False
    YIELD_ERRORS: bool = False

    def __init__(self, filename: str):
        super().__init__(filename)


    @staticmethod
    def error_checker(value):
        if isinstance(value, SSCException):
            return True
        return False

    @staticmethod
    def get_text_description(outputs):
        if isinstance(outputs, dict):
            return "{0}\t|\t{1}\t|\t{2}\t|\t{3:.3f} ms\t|\t???\t".format(
                *outputs.values()
            )
        elif isinstance(outputs, list):
            result = ""
            for output in outputs:
                result += "{0}\t|\t{1}\t|\t{2}\t|\t{3:.3f} ms\t|\t{4}\t|\t{5}\n".format(
                    *output.values()
                )
            if result[-1:] == "\n":
                return result[:-1]
            return result

    def __call__(self):
        for reader in super().__call__():
            if self.error_checker(self.input_error_status) and not self.IGNORE_ERRORS:
                yield str(self.input_error_status)
                return
            else:
                worker = Controller(reader)()
                if self.error_checker(worker):
                    if self.YIELD_ERRORS:
                        yield str(worker)
                if worker is not None:
                    yield self.get_text_description(worker)

    def __str__(self):
        return "[{0}]".format(", ".join([str(obj) for obj in self.units]))

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)
