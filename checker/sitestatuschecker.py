from checker.units.controller import Controller
from checker.units.exceptions import SSCException, FileInvalidFormat
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
            return "\t|\t{0}\t|\t{1}\t|\t{2:.3f} ms\t|\t???\t".format(
                *outputs.values()
            )
        elif isinstance(outputs, list):
            result = []
            for output in outputs:
                result.append(
                    "\t|\t{0}\t|\t{1}\t|\t{2:.3f} ms\t|\t{3}\t|\t{4}".format(
                        *output.values()
                    )
                )
            return result

    def __call__(self):
        if isinstance(self.input_error_status, SSCException):
            if isinstance(self.input_error_status, FileInvalidFormat) or not self.IGNORE_ERRORS:
                yield self.input_error_status
                return
            if self.YIELD_ERRORS:
                yield self.input_error_status

        for reader in super().__call__():
            worker = Controller(reader)()
            if self.error_checker(worker):
                yield worker
                continue
            if worker is not None:
                yield self.get_text_description(worker)

    def __str__(self):
        return "[{0}]".format(", ".join([str(obj) for obj in self.units]))

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)
