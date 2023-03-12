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
import os
import sys
import schedule

from datetime import datetime

from checker.config import *
from checker.sitestatuschecker import SiteStatusChecker
from checker.units.exceptions import SSCException, FileInvalidFormat, DataInvalidFormat

__all__ = (
    "Display",
)

class Display(object):
    r"""
    Class for passing data to the console and for periodically starting workers

    get_file_name() -> None
        A function to get the file name and to initialize the worker
    create_schedule() -> None
        A function to create a schedule for checking sites
        (the function creates a schedule that runs the show function every hour)
    show() -> None
        Calls one iteration of the worker
    """
    __slots__ = (
        "worker", "ignore_errors"
    )
    def __init__(self) -> None:
        self.worker = None
        self.ignore_errors = False
        self.get_file_name()

    def get_file_name(self) -> None:
        r"""
        A function to get the file name and to initialize the worker

        :return: None
        """
        filename = input(f"{self.get_time()} [INFO]: Enter filename (csv): ")
        if not os.path.exists(filename):
            print(f"{self.get_time()} [ERROR]: File is not exists")
            self.get_file_name()
            return
        self.ignore_errors = True if input(f"{self.get_time()} [INFO]: Ignore errors in csv? (Y/N): ").lower() == "y" else False
        print_errors = False
        if self.ignore_errors:
            print_errors = True if input(f"{self.get_time()} [INFO]: Print errors? (Y/N): ").lower() == "y" else False

        worker = SiteStatusChecker(filename)
        worker.IGNORE_ERRORS = self.ignore_errors
        worker.YIELD_ERRORS = print_errors

        self.worker = worker
        print(f"{self.get_time()} [INFO]: Worker created")

    def create_schedule(self) -> None:
        r"""
        A function to create a schedule for checking sites
        (the function creates a schedule that runs the show function every hour)

        :return: None
        """
        self.show()
        schedule.every().hour.do(self.show)
        while True:
            schedule.run_pending()

    @staticmethod
    def get_time():
        return datetime.now().strftime(DATE_FORMAT)

    def show(self) -> None:  # there was logging but requests warnings killed it:(
        r"""
        Calls one iteration of the worker

        :return: None
        """
        print(f"{self.get_time()} [INFO]: Check starting...")
        for i in self.worker():
            if isinstance(i, list):
                for j in i:
                    if j is not None:
                        self.__send(j)
                continue

            if i is not None:
                self.__send(i)
        print(f"{self.get_time()} [INFO]: Check completed!")

    def __send(self, value) -> None:
        if isinstance(value, DataInvalidFormat):
            print(f"{self.get_time()} [ERROR]:", value)
            if not self.ignore_errors:
                sys.exit(1)
            print(f"{self.get_time()} [INFO]: continue...")
        elif isinstance(value, FileInvalidFormat):
            print(f"{self.get_time()} [CRITICAL]:", value)
            sys.exit(1)
        elif isinstance(value, SSCException):
            print(f"{self.get_time()} [WARNING]:", value)
        else:
            print(f"{self.get_time()} [INFO]:", value)
