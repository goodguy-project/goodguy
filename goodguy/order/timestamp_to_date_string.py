import datetime
import time
from typing import Union


def timestamp_to_date_string(ts: Union[int, float]) -> str:
    dt = datetime.datetime.fromtimestamp(ts)
    return '%d.%02d.%02d %02d:%02d' % (dt.year, dt.month, dt.day, dt.hour, dt.minute)


if __name__ == '__main__':
    print(timestamp_to_date_string(time.time()))
