# -*- coding:utf-8 -*-
import sys
import logging

from checker import Display

if __name__ == "__main__":
    if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 10):
        logging.critical("Python version must be >= than 3.10")
        sys.exit(1)
    try:
        app = Display()
        app.create_schedule()
    except Exception as e:
        logging.critical(f"{e.__class__.__name__}({e.args[0]})")
        # raise e