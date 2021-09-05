import logging
import time

from loguru import logger

from goodguy.service.crawl import get_recent_contest
from goodguy.timer.contest.email_job import send_contest_remind_email
from goodguy.timer.contest.feishu_job import send_contest_feishu_message
from goodguy.util.config import GLOBAL_CONFIG as GBC
from goodguy.util.go import go
from goodguy.util.const import PLATFORM_ALL


def contest_job() -> None:
    @go(daemon=True)
    def contest_job_with_platform(platform: str):
        data = get_recent_contest(platform)
        now = time.time()
        for contest in data.recent_contest:
            # 如果比赛在两个小时以内进行
            if now < contest.timestamp < now + 2 * 60 * 60:
                logger.debug(data)
                # 比赛前一小时发送邮件提醒
                if GBC.get(f"{platform}.email_remind", False) or GBC.get("all_email_remind", False):
                    send_contest_remind_email(contest.timestamp - 60 * 60)
                # 比赛前一个小时发送飞书提醒
                if GBC.get(f"{platform}.feishu_remind", False) or GBC.get(f"all_feishu_remind", False):
                    send_contest_feishu_message(contest.timestamp - 60 * 60, contest, platform)

    tasks = [contest_job_with_platform(pf) for pf in PLATFORM_ALL]
    for task in tasks:
        task.get()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    contest_job()
