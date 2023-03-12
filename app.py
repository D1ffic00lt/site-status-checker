# -*- coding:utf-8 -*-
import sys

from checker import Display

if __name__ == "__main__":
    # if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 10):
    #     print(f"CRITICAL ERROR: Python version must be >= than 3.10")
    #     sys.exit(1)
    try:
        app = Display()
        app.create_schedule()

    except Exception as e:
        print(f"CRITICAL ERROR: {e.__class__.__name__}({e.args[0]})")
