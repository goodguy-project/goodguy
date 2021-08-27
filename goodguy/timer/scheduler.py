from apscheduler.schedulers.background import BackgroundScheduler

from goodguy.util.config import GLOBAL_CONFIG

_SCHEDULER = BackgroundScheduler(timezone=GLOBAL_CONFIG.get("timezone", "Asia/Shanghai"))
_SCHEDULER.start()


def scheduler() -> BackgroundScheduler:
    global _SCHEDULER
    return _SCHEDULER
