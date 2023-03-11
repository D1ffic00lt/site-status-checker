import requests

from time import sleep
from functools import wraps
from typing import Union

class IgnoreInternetExceptions(object):
    __slots__ = (
        "check_ip",
    )
    def __init__(self, check_ip: bool = False) -> None:
        self.check_ip = check_ip

    def __repr__(self) -> str:
        return "{}()".format(self.__class__.__name__)

    @staticmethod
    def check_internet_connection() -> Union[bool, requests.Response]:
        try:
            requests.head("http://www.google.com/", timeout=3)
        except requests.ConnectionError:
            return False
        return True

    def __call__(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if not self.check_internet_connection():
                sleep(3)
                return InternetConnectionError()

            try:
                result = func(*args, **kwargs)
            except requests.exceptions.ConnectionError:
                if self.check_ip:
                    return False
            else:
                return result
        return decorator


class SSCException(Exception):
    def __init__(self, message: str = ""):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return "{}".format(self.message)

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, self.message)


class CSVReaderException(SSCException):
    def __init__(self, message: str = ""):
        super().__init__(message)

class DataInvalidFormat(CSVReaderException):
    def __init__(self, message: str = ""):
        super().__init__(message)

class FileInvalidFormat(CSVReaderException):
    def __init__(self, message: str = ""):
        super().__init__(message)

class CheckerException(SSCException):
    def __init__(self, message: str = ""):
        super().__init__(message)

class InternetConnectionError(CheckerException):
    def __init__(self, message: str = ""):
        super().__init__(message)