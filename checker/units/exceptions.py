# -*- coding:utf-8 -*-
"""
The MIT License (MIT)
Copyright (c) 2023-present Dmitry Filinov (D1ffic00lt)
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import requests

from time import sleep
from functools import wraps

__all__ = (
    "IgnoreInternetExceptions", "SSCException",
    "CSVReaderException", "DataInvalidFormat",
    "FileInvalidFormat", "CheckerException",
    "InternetConnectionError"
)

class IgnoreInternetExceptions(object):
    __slots__ = (
        "check_ip",
    )
    def __init__(self, check_ip: bool = False) -> None:
        self.check_ip = check_ip

    def __repr__(self) -> str:
        return "{}()".format(self.__class__.__name__)

    @staticmethod
    def __check_internet_connection() -> bool:
        try:
            requests.head("http://www.google.com/", timeout=3)
        except requests.ConnectionError:
            return False
        return True

    def __call__(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if not self.__check_internet_connection():
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
    __slots__ = (
        "message",
    )
    def __init__(self, message: str = ""):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return "{0}".format(self.message)

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

class InternetConnectionError(SSCException):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def __str__(self):
        return "No internet connection! ({0})".format(self.__class__.__name__)