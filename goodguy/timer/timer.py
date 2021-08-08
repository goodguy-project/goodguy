import logging
import time

from goodguy.timer.contest.contest_job import contest_job
from goodguy.util.config import GLOBAL_CONFIG
from goodguy.util.go import go


@go(daemon=True)
def job() -> None:
    logging.info('job start')
    contest_job()


def sync_timer():
    while True:
        job()
        # 任务周期进行时间 默认45分钟
        time.sleep(GLOBAL_CONFIG.get("timer.interval", 2700))


@go(daemon=True)
def async_timer():
    sync_timer()
