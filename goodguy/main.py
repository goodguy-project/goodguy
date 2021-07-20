import asyncio
import logging

from goodguy.feishu.serve import serve as feishu_serve
from goodguy.timer.timer import timer
from goodguy.util.config import GLOBAL_CONFIG


async def main():
    logging.getLogger().setLevel(GLOBAL_CONFIG.get("loglevel"))
    await asyncio.gather(feishu_serve(), timer())


if __name__ == '__main__':
    asyncio.run(main())
