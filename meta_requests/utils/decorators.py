import warnings
from functools import wraps


def disable_warnings(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = func(*args, **kwargs)
        return res

    return inner
