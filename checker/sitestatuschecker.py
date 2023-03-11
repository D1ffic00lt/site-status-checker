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
from typing import Union, Any

from checker.units.controller import Controller
from checker.units.exceptions import SSCException, FileInvalidFormat
from checker.units.reader import CSVReader

__all__ = (
    "SiteStatusChecker",
)

class SiteStatusChecker(CSVReader):
    IGNORE_ERRORS: bool = False
    YIELD_ERRORS: bool = False

    def __init__(self, filename: str) -> None:
        super().__init__(filename)


    @staticmethod
    def error_checker(value: Any) -> bool:
        if isinstance(value, SSCException):
            return True
        return False

    @staticmethod
    def get_text_description(outputs: Union[dict, list]) -> str:
        if isinstance(outputs, dict):
            return "host: {0}\t|\tip: {1}\t|\tRTT: {2:.3f} ms\t|\tport: ???\t|\tmulty ip: {3}".format(
                *outputs.values()
            )
        else:
            result = []

            for output in outputs:
                if len(output.values()) == 6:
                    result.append(
                        "host: {0}\t|\tip: {1}\t|\tRTT: {2:.3f} ms\t|\tport: {3}\t|\tstatus: {4}\t|\tmulty ip: {5}".format(
                            *output.values()
                        )
                    )
                else:
                    result.append(
                        "host: {0}\t|\tip: {1}\t|\tRTT: {2:.3f} ms\t|\tport: ???\t|\tmulty ip: {3}".format(
                            *output.values()
                        )
                    )

            return result

    def __call__(self) -> Any:
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

    def __str__(self) -> str:
        return "[{0}]".format(", ".join([str(obj) for obj in self.units]))

    def __repr__(self) -> str:
        return "{0}()".format(self.__class__.__name__)
