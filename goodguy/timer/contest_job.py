import asyncio
import datetime
import os
import random
import time
from threading import Lock
from typing import List, Dict

from cachetools.func import ttl_cache
from jinja2 import Template

from goodguy.feishu.send_message import send_card_message
from goodguy.pb import crawl_service_pb2
from goodguy.service.crawl import get_recent_contest
from goodguy.timer.scheduler import scheduler
from goodguy.util.config import GLOBAL_CONFIG
from goodguy.util.platform_all import PLATFORM_ALL
from goodguy.util.send_all_email import send_all_email


# 获取email内容
def get_contest_email(cts: List[crawl_service_pb2.RecentContest]) -> str:
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, 'contest_email.html'), 'r', encoding='utf-8') as file:
        e = file.read()
    template = Template(e)
    contests = []
    now = time.time()
    for c in cts:
        if c.timestamp < now + 60 * 60 + 10:
            contests.append({
                "color": "red",
                "message": "Message TODO",
            })
    return template.render(contests)


_last_send = 0
_last_send_lock = Lock()


# 定时任务
def remind_email_sender() -> None:
    async def crawl_job(platform: str) -> crawl_service_pb2.RecentContest:
        return get_recent_contest(platform)

    global _last_send, _last_send_lock
    tasks = [crawl_job(pf) for pf in PLATFORM_ALL]
    rsp = await asyncio.gather(tasks)
    cts = []
    # 遍历所有比赛
    for rc in rsp:
        for c in rc.recent_contest:
            cts.append(c)
    if len(cts) == 0:
        return
    cts.sort(key=lambda x: x.timestamp)
    # 校验
    # 如果下一场比赛开始时间是在接下来一个小时内 且之前一个小时内没有发送过此邮件 则进行邮件提醒
    now = time.time()
    ok = False
    with _last_send_lock:
        if _last_send + 60 * 60 - 10 < now:
            ok = True
            _last_send = now
    if ok and now < cts[0].timestamp < now + 60 * 60 + 10:
        send_all_email('html', get_contest_email(cts))


def send_contest_remind_email(ts: int) -> None:
    # 在时间戳ts时添加定时任务
    dt = datetime.datetime.fromtimestamp(ts)
    scheduler().add_job(
        remind_email_sender,
        trigger='date',
        args=(),
        run_date=dt,
    )


def gen_feishu_card_message() -> Dict:
    return dict()


def send_contest_feishu_message(contest: crawl_service_pb2.RecentContest.ContestMessage) -> None:
    def is_sent_message(name: str):
        @ttl_cache(ttl=18000)
        def message_manager(_: str, key: int) -> int:
            return key

        rd = random.getrandbits(128)
        return rd == message_manager(name, rd)

    if is_sent_message(contest.name):
        send_card_message(gen_feishu_card_message())


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

    tasks = [contest_job_with_platform(pf) for pf in PLATFORM_ALL]
    await asyncio.gather(*tasks)
