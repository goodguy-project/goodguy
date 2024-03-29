import asyncio
import datetime
import os
import time
from threading import Lock
from typing import List, Tuple, Dict

from jinja2 import Template
from loguru import logger

from goodguy.pb import crawl_service_pb2
from goodguy.service.crawl import get_recent_contest
from goodguy.timer.scheduler import scheduler
from goodguy.util.get_html_from_mjml import get_html_from_mjml
from goodguy.util.const import PLATFORM_ALL
from goodguy.util.send_email import send_all_email
from goodguy.util.timestamp_to_date_string import timestamp_to_date_string, duration_to_string


# 获取email内容
def get_contest_email(cts: List[Tuple[str, crawl_service_pb2.RecentContest]]) -> Tuple[str, str]:
    def get_email_object(pf: str, c: crawl_service_pb2.RecentContest, **kwargs) -> Dict[str, str]:
        start_dt = datetime.datetime.fromtimestamp(c.timestamp)
        end_dt: datetime.datetime = start_dt + datetime.timedelta(seconds=c.duration)
        t1, t2 = '%02d' % start_dt.hour, '%02d' % start_dt.minute
        t3, t4 = '%02d' % end_dt.hour, '%02d' % end_dt.minute
        if start_dt.date() != end_dt.date():
            t1 = str(start_dt.date()) + ' ' + t1
            t3 = str(end_dt.date()) + ' ' + t3
        return {
            **kwargs,
            "name": c.name,
            "url": c.url,
            "start": timestamp_to_date_string(c.timestamp),
            "end": timestamp_to_date_string(end_dt.timestamp()),
            "t1": t1,
            "t2": t2,
            "t3": t3,
            "t4": t4,
            "platform": pf,
            "duration": duration_to_string(c.duration),
        }

    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, 'contest_email.jinja2'), 'r', encoding='utf-8') as file:
        e = file.read()
    template = Template(e)
    urgent = []
    common = []
    not_urgent = []
    now = time.time()
    for pf, c in cts:
        # 一天内的比赛
        if now - 60 * 60 - 10 < c.timestamp < now + 60 * 60 + 10:
            urgent.append(get_email_object(pf, c))
        elif c.timestamp < now + 60 * 60 * 24 + 10:
            common.append(get_email_object(pf, c))
        elif c.timestamp >= now + 60 * 60 * 24 + 10:
            not_urgent.append(get_email_object(pf, c))
    mjml = template.render({
        "urgent": urgent,
        "common": common,
        "not_urgent": not_urgent,
    })
    html = get_html_from_mjml(mjml)
    return f'GoodGuy - 最近比赛提醒（{len(cts)}条）', html


_LAST_SEND = 0
_LAST_SEND_LOCK = Lock()


# 定时任务
def remind_email_sender() -> None:
    async def crawl_jobs():
        async def crawl_job(platform: str) -> Tuple[str, crawl_service_pb2.RecentContest]:
            return platform, get_recent_contest(platform)

        tasks = [crawl_job(pf) for pf in PLATFORM_ALL]
        return await asyncio.gather(*tasks)

    global _LAST_SEND, _LAST_SEND_LOCK
    rsp = asyncio.run(crawl_jobs())
    ok = False
    cts = []
    now = time.time()
    # 遍历所有比赛
    for pf, rc in rsp:
        for c in rc.recent_contest:
            # 结束时间大于当前时间才可以被写进邮件中
            if c.timestamp + c.duration >= time.time():
                cts.append((pf, c))
                # 有一场比赛是在接下来一个小时内开始才写进邮件中
                if now <= c.timestamp <= now + 60 * 60 + 10:
                    ok = True
    if len(cts) == 0 or not ok:
        return
    cts.sort(key=lambda x: x[1].timestamp)
    ok = False
    # 12小时内没有发送过邮件才可再发一次邮件
    with _LAST_SEND_LOCK:
        if _LAST_SEND + 60 * 60 * 12 - 10 < now:
            ok = True
            _LAST_SEND = now
    if ok:
        title, text = get_contest_email(cts)
        logger.debug(text)
        send_all_email('html', title, text)


def send_contest_remind_email(ts: int) -> None:
    # 在时间戳ts时添加定时任务
    dt = datetime.datetime.fromtimestamp(ts)
    scheduler().add_job(
        remind_email_sender,
        trigger='date',
        args=(),
        run_date=dt,
    )


if __name__ == '__main__':
    # logging.getLogger().setLevel(logging.DEBUG)
    remind_email_sender()
