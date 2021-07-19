import asyncio
import logging

from goodguy.feishu.serve import serve as feishu_serve
from goodguy.util.config import GLOBAL_CONFIG


def main():
    logging.getLogger().setLevel(GLOBAL_CONFIG.get("loglevel"))
    asyncio.run(feishu_serve())


if __name__ == '__main__':
    main()
