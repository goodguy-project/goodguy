from apscheduler.schedulers.background import BackgroundScheduler

from goodguy.util.config import GLOBAL_CONFIG

_scheduler = BackgroundScheduler(timezone=GLOBAL_CONFIG.get("timezone", "Asia/Shanghai"))
_scheduler.start()


def scheduler() -> BackgroundScheduler:
    global _scheduler
    return _scheduler
