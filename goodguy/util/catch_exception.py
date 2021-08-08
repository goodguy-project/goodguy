import logging


def catch_exception(ret=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                ans = func(*args, **kwargs)
                logging.debug(ans)
                return ans
            except Exception as e:
                logging.exception(e)
            return ret

        return wrapper

    return decorator
