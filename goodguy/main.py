import asyncio
import logging
import os

from loguru import logger

from goodguy.feishu.serve import serve as feishu_serve
from goodguy.timer.timer import async_timer
from goodguy.util.config import GLOBAL_CONFIG
from goodguy.util.const import ROOT


async def main():
    logger.add(os.path.join(ROOT, 'goodguy.log'),
               retention='14 days', rotation='12:00')
    logging.getLogger().setLevel(GLOBAL_CONFIG.get("loglevel", logging.ERROR))
    async_timer()
    await feishu_serve()


if __name__ == '__main__':
    asyncio.run(main())
