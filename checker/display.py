# -*- coding:utf-8 -*-
import os
import sys
import warnings
import schedule
import logging

from checker.sitestatuschecker import SiteStatusChecker
from checker.units.config import *
from checker.units.exceptions import SSCException, FileInvalidFormat, DataInvalidFormat


class Display(object):
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
        logging.basicConfig(format=FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)
        handler = logging.FileHandler(LOG_PATH, mode='+a')
        handler.setFormatter(logging.Formatter(FORMAT))
        logging.getLogger().addHandler(handler)
        logging.info("Start logging")
        warnings.filterwarnings("ignore")
        logging.info("Set filterwarnings ignore")

    def send(self, value) -> None:
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

    def get_file_name(self) -> None:
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
        self.show()
        schedule.every().hour.do(self.show)
        while True:
            schedule.run_pending()

    def show(self) -> None:
        logging.info("Check starting...")
        for i in self.worker():
            if isinstance(i, list):
                for j in i:
                    if j is not None:
                        self.send(j)
                continue

            if i is not None:
                self.send(i)
        logging.info("Check completed!")