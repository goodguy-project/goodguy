import os
from copy import deepcopy

import yaml
from readerwriterlock.rwlock import RWLockReadD


class Config(object):
    __path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.yml')
    __lock = RWLockReadD()
    __conf = None

    @classmethod
    def reload_config(cls) -> None:
        with open(cls.__path, 'r', encoding='utf-8') as config_file:
            conf = yaml.load(config_file.read(), yaml.FullLoader)
        with cls.__lock.gen_wlock():
            cls.__conf = conf

    @classmethod
    def get(cls, path: str, default=None):
        if cls.__conf is None:
            cls.reload_config()
        args = path.split('.')
        with cls.__lock.gen_rlock():
            ret = cls.__conf
            for arg in args:
                if arg == '':
                    continue
                try:
                    if isinstance(ret, list):
                        arg = int(arg)
                    ret = ret[arg] # pylint: disable=unsubscriptable-object
                except (KeyError, ValueError, IndexError, TypeError):
                    return default
            if ret is None:
                return default
            return deepcopy(ret)


if __name__ == '__main__':
    print(Config.get("apple.a.2"))
