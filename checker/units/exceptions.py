import requests

from functools import wraps

class IgnoreInternetExceptions(object):
    def __init__(self):
        pass

    def __repr__(self):
        return "IgnoreInternetExceptions()"

    def __call__(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ConnectionError:
                return "ConnectionError"
        return decorator
