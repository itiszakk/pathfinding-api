"""
Timing module
"""

import time
from functools import wraps


def time_in_milliseconds() -> int:
    """
    Return the current time in milliseconds since the Epoch
    :return: milliseconds
    """
    return round(time.time() * 1000)


def timing(message):
    """
    Decorator function for measuring the execution time of a wrapped function
    :param message: the message to display along with the timing information
    :return: decorator function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time_in_milliseconds()
            result = func(*args, **kwargs)
            end_time = time_in_milliseconds()

            print(f'{message}: {end_time - start_time} ms')

            return result

        return wrapper

    return decorator
