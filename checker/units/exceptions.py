import requests

from functools import wraps


class IgnoreInternetExceptions(object):
    def __init__(self, check_ip: bool = False):
        self.check_ip = check_ip

    def __repr__(self):
        return "IgnoreInternetExceptions()"

    def __call__(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if self.check_ip:
                    return True
                return result
            except requests.exceptions.ConnectionError:
                if self.check_ip:
                    return False
                return "ConnectionError"

        return decorator
