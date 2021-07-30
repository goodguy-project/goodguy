import asyncio
import logging

from goodguy.feishu.serve import serve as feishu_serve
from goodguy.timer.timer import async_timer
from goodguy.util.config import GLOBAL_CONFIG


async def main():
    logging.getLogger().setLevel(GLOBAL_CONFIG.get("loglevel", logging.ERROR))
    async_timer()
    await feishu_serve()


if __name__ == '__main__':
    asyncio.run(main())
