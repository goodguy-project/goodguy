import asyncio
import logging

from goodguy.timer.contest.contest_job import contest_job
from goodguy.util.config import GLOBAL_CONFIG
from goodguy.util.go import go


async def job() -> None:
    logging.info('job start')
    await contest_job()


async def timer():
    while True:
        task = asyncio.create_task(job())
        # 任务周期进行时间 默认45分钟
        await asyncio.sleep(GLOBAL_CONFIG.get("timer.interval", 2700))
        # 无论任务是否做完 都应该停掉
        task.cancel()


def sync_timer():
    asyncio.run(timer())


@go(daemon=True)
def async_timer():
    sync_timer()
