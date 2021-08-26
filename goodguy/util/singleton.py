from threading import Lock
from typing import Optional


def singleton(*args, **kwargs):
    def decorator(cls):
        instance: Optional[cls] = None
        lock = Lock()

        def get_instance() -> cls:
            nonlocal instance, lock
            if instance is None:
                with lock:
                    if instance is None:
                        instance = cls(*args, **kwargs)
            return instance

        cls.get_instance = get_instance
        return cls

    return decorator
