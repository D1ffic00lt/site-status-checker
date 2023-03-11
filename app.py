# -*- coding:utf-8 -*-
import logging

from checker import Display

if __name__ == "__main__":
    try:
        app = Display()
        app.create_schedule()
    except Exception as e:
        logging.critical(f"{e.__class__.__name__}({e.args[0]})")
        raise e