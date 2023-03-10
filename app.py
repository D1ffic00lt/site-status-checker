import logging

from checker.display import Display

if __name__ == "__main__":
    try:
        app = Display()
        app.create_schedule()
    except Exception as e:
        logging.critical(f"{e.__class__.__name__}: {e.args[0]}")