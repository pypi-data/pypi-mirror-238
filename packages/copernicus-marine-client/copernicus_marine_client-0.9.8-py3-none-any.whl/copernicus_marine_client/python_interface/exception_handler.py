from functools import wraps
from typing import Callable

import click


def log_exception_and_exit(function: Callable):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except click.Abort:
            print("Abort")
        except Exception as exception:
            raise exception

    return wrapper
