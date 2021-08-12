import asyncio
import logging
import os

from loguru import logger

from goodguy.feishu.serve import serve as feishu_serve
from goodguy.timer.timer import async_timer
from goodguy.util.config import GLOBAL_CONFIG
from goodguy.util.const import ROOT


def log_init():
    level = {
        logging.CRITICAL: 'CRITICAL',
        logging.ERROR: 'ERROR',
        logging.WARNING: 'WARNING',
        logging.INFO: 'INFO',
        logging.DEBUG: 'DEBUG',
    }.get(GLOBAL_CONFIG.get("loglevel", logging.ERROR), 'ERROR')
    logger.add(os.path.join(ROOT, 'goodguy.log'), retention='14 days', rotation='12:00', level=level)
    logging.getLogger().setLevel(GLOBAL_CONFIG.get("loglevel", logging.ERROR))


async def main():
    log_init()
    async_timer()
    await feishu_serve()


if __name__ == '__main__':
    asyncio.run(main())
