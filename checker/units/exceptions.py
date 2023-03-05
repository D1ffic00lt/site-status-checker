import requests

from time import sleep
from functools import wraps


class IgnoreInternetExceptions(object):
    def __init__(self, check_ip: bool = False):
        self.check_ip = check_ip

    def __repr__(self):
        return "IgnoreInternetExceptions()"

    def __call__(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except requests.exceptions.ConnectionError:
                if self.check_ip:
                    return False
                return "ConnectionError"

        return decorator


class SSCException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.message)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.message)


class CSVReaderException(SSCException):
    def __init__(self, message: str):
        super().__init__(message)


class CheckerException(SSCException):
    def __init__(self, message: str):
        super().__init__(message)
