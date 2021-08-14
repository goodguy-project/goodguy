import datetime
import time
from typing import Union


def timestamp_to_date_string(ts: Union[int, float]) -> str:
    dt = datetime.datetime.fromtimestamp(ts)
    return '%d-%02d-%02d %02d:%02d' % (dt.year, dt.month, dt.day, dt.hour, dt.minute)


def duration_to_string(duration: int) -> str:
    td = datetime.timedelta(seconds=duration)
    d = td.days
    h, r = divmod(td.seconds, 3600)
    h %= 24
    m, _ = divmod(r, 60)
    res = '%02d:%02d' % (h, m)
    if d != 0:
        res = f"{d}:{res}"
    return res


if __name__ == '__main__':
    print(timestamp_to_date_string(time.time()))
    print(duration_to_string(604860))
