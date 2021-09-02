import functools
import os
from inspect import isroutine
from threading import Semaphore
from typing import Union, Callable, Optional
from concurrent.futures import ThreadPoolExecutor


def _decorator_callable(call: Callable, max_worker: Optional[int] = None) -> Callable:
    exe = ThreadPoolExecutor(max_worker)

    def wrapper(*args, **kwargs):
        return exe.submit(call, *args, **kwargs).result()

    return wrapper


def _decorator_class(cls: type, max_worker: Optional[int] = None) -> type:
    if max_worker is None:
        max_worker = min(32, (os.cpu_count() or 1) + 4)

    class _SemaphoreRelease(object):
        def __init__(self, func: Callable, semaphore: Semaphore):
            self.func = func
            self.semaphore = semaphore

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

        def __del__(self):
            self.semaphore.release()

    class _PoolDecoratorClass(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__semaphore = Semaphore(max_worker)

        def __getattribute__(self, item):
            what = super().__getattribute__(item)
            if isroutine(what):
                self.__semaphore.acquire()
                return _SemaphoreRelease(what, self.__semaphore)
            return what

    return _PoolDecoratorClass


def _decorator(obj: Union[Callable, type], max_worker: Optional[int] = None) -> Union[Callable, type]:
    if isinstance(obj, type):
        return _decorator_class(obj, max_worker)
    return _decorator_callable(obj, max_worker)


def pool(max_worker: Union[Callable, type, int, None] = None) -> Union[Callable, type]:
    if isinstance(max_worker, int) or max_worker is None:
        return functools.partial(_decorator, max_worker=max_worker)
    return _decorator(max_worker)
