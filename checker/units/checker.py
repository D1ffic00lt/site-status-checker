from exceptions import IgnoreInternetExceptions
from reader import ReadObject


class Checker(object):
    def __init__(self, data: ReadObject):
        self.data: ReadObject = data

    def __repr__(self):
        return "Checker({0})".format(repr(self.data))

    @IgnoreInternetExceptions()
    def __call__(self):
        pass
