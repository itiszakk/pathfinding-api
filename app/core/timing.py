import time
from functools import wraps


def timing(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            print(f'{message}: {end_time - start_time} sec')

            return result

        return wrapper

    return decorator
