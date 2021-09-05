from goodguy.timer.feishu_calendar.feishu_calendar import Calendar

calendar = Calendar()

def calendar_job():
    calendar.delete_timeout_events(timeout=60 * 60 * 24 * 30)
    calendar.update_all_events()