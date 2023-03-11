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
import warnings
import schedule
import logging

from checker.config import *
from checker.sitestatuschecker import SiteStatusChecker
from checker.units.exceptions import SSCException, FileInvalidFormat, DataInvalidFormat

__all__ = (
    "Display",
)

class Display(object):
    r"""
    Class for passing data to the console and for periodically starting workers

    setup_logging() -> None
        The function is called when the class is initialized,
        it is intended for setting up the logging module and ignoring warnings
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
        self.setup_logging()
        self.get_file_name()

    @staticmethod
    def setup_logging() -> None:
        r"""
        The function is called when the class is initialized,
        it is intended for setting up the logging module and ignoring warnings

        :return: None
        """
        logging.basicConfig(format=FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)
        handler = logging.FileHandler(LOG_PATH, mode='+a')
        handler.setFormatter(logging.Formatter(FORMAT))
        logging.getLogger().addHandler(handler)
        logging.info("Start logging")
        warnings.filterwarnings("ignore")
        logging.info("Set filterwarnings ignore")

    def get_file_name(self) -> None:
        r"""
        A function to get the file name and to initialize the worker

        :return: None
        """
        logging.info("Enter filename (csv): ")
        filename = input()
        if not os.path.exists(filename):
            logging.info("File is not exists")
            self.get_file_name()
            return
        logging.info("Ignore errors in csv? (Y/N): ")
        self.ignore_errors = True if input().lower() == "y" else False
        print_errors = False
        if self.ignore_errors:
            logging.info("Print errors? (Y/N): ")
            print_errors = True if input().lower() == "y" else False

        worker = SiteStatusChecker(filename)
        worker.IGNORE_ERRORS = self.ignore_errors
        worker.YIELD_ERRORS = print_errors

        self.worker = worker
        logging.info("Worker created")

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

    def show(self) -> None:
        r"""
        Calls one iteration of the worker

        :return: None
        """
        logging.info("Check starting...")
        for i in self.worker():
            if isinstance(i, list):
                for j in i:
                    if j is not None:
                        self.__send(j)
                continue

            if i is not None:
                self.__send(i)
        logging.info("Check completed!")

    def __send(self, value) -> None:
        if isinstance(value, DataInvalidFormat):
            logging.error(value)
            if not self.ignore_errors:
                sys.exit(1)
            logging.info("continue...")
        elif isinstance(value, FileInvalidFormat):
            logging.critical(value)
            sys.exit(1)
        elif isinstance(value, SSCException):
            logging.warning(value)
        else:
            logging.info(value)