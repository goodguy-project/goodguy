import datetime
import random
import time
from threading import Lock
from typing import Dict

from cachetools import TTLCache

from goodguy.feishu.send_message import send_card_message
from goodguy.util.timestamp_to_date_string import timestamp_to_date_string
from goodguy.pb import crawl_service_pb2
from goodguy.timer.contest.data import select_all_feishu_chat_id
from goodguy.timer.scheduler import scheduler


def _gen_feishu_card_message(c: crawl_service_pb2.RecentContest.ContestMessage, pf: str) -> Dict:
    colors = ('blue', 'wathet', 'turquoise', 'green', 'yellow', 'orange', 'red', 'carmine', 'violet', 'purple',
              'indigo')
    element = [{
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": e,
        }
    } for e in (f"名称：{c.name}", f"时间：{timestamp_to_date_string(c.timestamp)}", f"链接：{c.url}")]
    return {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True,
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{pf}比赛提醒",
                },
                "template": random.choice(colors),
            },
            "elements": element,
        },
    }


_contest_cache = TTLCache(maxsize=1024, ttl=5 * 60 * 60)
_contest_cache_lock = Lock()


def _is_not_sent_message(name: str) -> bool:
    global _contest_cache, _contest_cache_lock
    with _contest_cache_lock:
        if _contest_cache.get(name) is None:
            _contest_cache[name] = 1
            return True
    return False


def remind_message_sender(contest: crawl_service_pb2.RecentContest.ContestMessage, platform: str):
    if _is_not_sent_message(contest.name):
        base = _gen_feishu_card_message(contest, platform)
        for chat_id in select_all_feishu_chat_id():
            request = base.copy()
            request["chat_id"] = chat_id
            send_card_message(request)


def send_contest_feishu_message(ts: int, contest: crawl_service_pb2.RecentContest.ContestMessage, platform: str) -> None:
    # 在时间戳ts时添加定时任务
    dt = datetime.datetime.fromtimestamp(ts)
    scheduler().add_job(
        remind_message_sender,
        trigger='date',
        args=(contest, platform),
        run_date=dt,
    )


if __name__ == '__main__':
    remind_message_sender(crawl_service_pb2.RecentContest.ContestMessage(
        name="name",
        url="url",
        timestamp=int(time.time()),
    ), 'codeforces')
