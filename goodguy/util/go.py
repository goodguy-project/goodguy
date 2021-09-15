# 异步函数装饰器
# 加上了该装饰器后函数从同步变成异步
# 如果是类加上了该装饰器后这个类的使用__getattribute__调用的函数都会变成异步
# 异步的函数返回_Promise类对象 使用get函数可以获取结果
import functools
import threading
from inspect import isroutine
from typing import Callable, Union
import multiprocessing as mp


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


class _Process(mp.Process):
    def __init__(self, func: Callable, daemon: bool, args, kwargs):
        super().__init__()
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
        self.res = None
        self.que = mp.Queue()

    def run(self) -> None:
        self.que.put(self.__func(*self.__args, **self.__kwargs))

    def join(self):
        self.res = self.que.get()
        super().join()


class _Promise(object):
    def __init__(self, thread: _Thread):
        self.__thread = thread
        self.__thread.start()

    def get(self):
        self.__thread.join()
        return self.__thread.res


def _decorator_function(func: Callable, daemon: bool, use_process: bool) -> Callable:
    def wrapper(*args, **kwargs) -> _Promise:
        if use_process:
            return _Promise(_Process(func, daemon, args, kwargs))
        else:
            return _Promise(_Thread(func, daemon, args, kwargs))

    return wrapper


def _decorator_class(cls: type, daemon: bool, use_process: bool) -> Callable:
    class _GoDecorator(cls):
        def __getattribute__(self, item):
            what = super().__getattribute__(item)
            if isroutine(what):
                return _decorator_function(what, daemon, use_process)
            return what

    return _GoDecorator


def _decorator(obj: Callable, daemon: bool, use_process: bool) -> Callable:
    if isinstance(obj, type):
        return _decorator_class(obj, daemon, use_process)
    return _decorator_function(obj, daemon, use_process)


def go(daemon: Union[bool, Callable] = True, use_process: bool = False):  # pylint: disable=invalid-name
    if callable(daemon):
        return _decorator(daemon, True, use_process)
    return functools.partial(_decorator, daemon=daemon, use_process=use_process)
