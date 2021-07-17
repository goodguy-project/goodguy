import os
import yaml
from copy import deepcopy
from readerwriterlock.rwlock import RWLockFairD


class Config(object):
    def __init__(self, path: str):
        self.__lock = RWLockFairD()
        self.__conf = None
        self.__path = path
        self.reload_config(path)

    def reload_config(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as config_file:
            conf = yaml.load(config_file.read(), yaml.FullLoader)
        with self.__lock.gen_wlock():
            self.__conf = conf

    def get(self, path: str, default=None):
        args = path.split('.')
        with self.__lock.gen_rlock():
            ret = self.__conf
            for arg in args:
                if arg == '':
                    continue
                if ret is None:
                    return default
                try:
                    ret = ret[arg]
                except:
                    return default
            return deepcopy(ret)


GLOBAL_CONFIG = Config(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.yml'))


if __name__ == '__main__':
    print(GLOBAL_CONFIG.get("apple"))
