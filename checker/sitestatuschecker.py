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
    r"""
    Adapter class whose main function is to transform
    the output of the controller for the Display class

    IGNORE_ERRORS: bool = False
        parameter responsible for ignoring errors in
        data from the .csv file (excluding critical errors)
    YIELD_ERRORS: bool = False
        the parameter is responsible for displaying errors
        from the contents of the .csv file

    error_checker(value: Any) -> bool
        the function checks the value argument for
        belonging to the parent error class (SSCException)
    get_text_description(outputs: Union[dict, list]) -> str
        adapts controller output to console output
    __call__() -> Any
        Calls one iteration of the worker
    """
    IGNORE_ERRORS: bool = False
    YIELD_ERRORS: bool = False

    def __init__(self, filename: str) -> None:
        super().__init__(filename)


    @staticmethod
    def error_checker(value: Any) -> bool:
        r"""
        The function checks the value argument for
        belonging to the parent error class (SSCException)

        Parameters
        ------------
            value: Any
                value to check for belonging to an error class

        Returns
        --------
            returns the error status of the value (bool)
        """
        if isinstance(value, SSCException):
            return True
        return False

    @staticmethod
    def get_text_description(outputs: Union[dict, list]) -> str:
        r"""
        Adapts controller output to console output

        Parameters
        ------------
            outputs: Union[dict, list]
                controller's iteration result

        Returns
        --------
           returns a textual representation of the controller's iteration result (str)
        """
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
                elif "ssl" in output.keys():
                    result.append(
                        "host: {0}\t|\tip: {1}\t|\tRTT: {2:.3f} ms\t|\tport: {3}\t"
                        "|\tstatus: {4}\t|\tmulty ip: {5}\t|\tssl: {6}".format(
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
        r"""
        Runs all iterations of the worker

        Returns
        --------
           Returns the generator from the full cycle of the worker's execution (Any)
        """
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
