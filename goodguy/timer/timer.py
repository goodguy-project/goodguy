import asyncio

from goodguy.service.crawl import get_recent_contest
from goodguy.util.config import GLOBAL_CONFIG
from goodguy.util.platform_all import PLATFORM_ALL


async def contest_job() -> None:
    async def contest_job_with_platform(platform: str) -> None:
        task = await get_recent_contest(platform)
        # TODO add reminder
        # reminder with send checker
        # better with merger

    tasks = [contest_job_with_platform(pf) for pf in PLATFORM_ALL]
    await asyncio.gather(*tasks)


async def job() -> None:
    await contest_job()


async def timer():
    while True:
        await job()
        await asyncio.sleep(GLOBAL_CONFIG.get("timer.interval", 3600))
