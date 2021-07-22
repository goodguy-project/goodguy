import asyncio
import time

from goodguy.service.crawl import get_recent_contest
from goodguy.timer.contest.email_job import send_contest_remind_email
from goodguy.timer.contest.feishu_job import send_contest_feishu_message
from goodguy.util.config import GLOBAL_CONFIG
from goodguy.util.platform_all import PLATFORM_ALL


async def contest_job() -> None:
    async def contest_job_with_platform(platform: str) -> None:
        data = get_recent_contest(platform)
        now = time.time()
        for contest in data.recent_contest:
            # 如果比赛在两个小时以内进行
            if now < contest.timestamp < now + 2 * 60 * 60:
                # 比赛前一小时发送邮件提醒
                if GLOBAL_CONFIG.get(f"{platform}.email_remind", False):
                    send_contest_remind_email(contest.timestamp - 60 * 60)
                # 比赛前一个小时发送飞书提醒
                if GLOBAL_CONFIG.get(f"{platform}.feishu_remind", False):
                    send_contest_feishu_message(contest.timestamp - 60 * 60, contest)

    tasks = [contest_job_with_platform(pf) for pf in PLATFORM_ALL]
    await asyncio.gather(*tasks)
