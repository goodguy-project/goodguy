import datetime
from threading import Lock
from typing import Dict

from cachetools import TTLCache

from goodguy.feishu.send_message import send_card_message
from goodguy.pb import crawl_service_pb2
from goodguy.timer.scheduler import scheduler


def _gen_feishu_card_message() -> Dict:
    return dict()


_contest_cache = TTLCache(maxsize=1024, ttl=5 * 60 * 60)
_contest_cache_lock = Lock()


def _is_not_sent_message(name: str) -> bool:
    global _contest_cache, _contest_cache_lock
    with _contest_cache_lock:
        if _contest_cache.get(name) is None:
            _contest_cache[name] = 1
            return True
    return False


def remind_message_sender(contest: crawl_service_pb2.RecentContest.ContestMessage):
    if _is_not_sent_message(contest.name):
        send_card_message(_gen_feishu_card_message())


def send_contest_feishu_message(ts: int, contest: crawl_service_pb2.RecentContest.ContestMessage) -> None:
    # 在时间戳ts时添加定时任务
    dt = datetime.datetime.fromtimestamp(ts)
    scheduler().add_job(
        remind_message_sender,
        trigger='date',
        args=(contest,),
        run_date=dt,
    )
