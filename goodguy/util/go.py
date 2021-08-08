import threading
from typing import Callable


class _Thread(threading.Thread):
    def __init__(self, func: Callable, daemon: bool, args, kwargs):
        super().__init__()
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
        self.res = None
        self.setDaemon(daemon)

    def run(self) -> None:
        self.res = self.__func(*self.__args, **self.__kwargs)


class _Promise(object):
    def __init__(self, thread: _Thread):
        self.__thread = thread
        self.__thread.start()

    def get(self):
        self.__thread.join()
        return self.__thread.res


def go(daemon: bool = False):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs) -> _Promise:
            return _Promise(_Thread(func, daemon, args, kwargs))

        return wrapper

    return decorator
