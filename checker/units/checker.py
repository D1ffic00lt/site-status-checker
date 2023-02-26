from reader import CSVReader


class Checker(object):
    def __init__(self, data: CSVReader):
        self.data: CSVReader = data

    def __repr__(self):
        return "Checker({0})".format(repr(self.data))

    def __call__(self):
        if self.data.input_error_status:
            return Exception("Error")
