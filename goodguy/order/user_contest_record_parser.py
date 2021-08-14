import datetime
import os
import random
import time
from threading import Lock
from typing import Dict

import matplotlib.pyplot as plt

from goodguy.feishu.upload_image import upload_image
from goodguy.pb import crawl_service_pb2
from goodguy.util.const import ROOT


def user_contest_record_parser(handle: str, platform: str,
                               user_contest_record: crawl_service_pb2.UserContestRecord) -> str:
    return "\n".join([f"{key}: {value}" for key, value in (
        ('handle', handle),
        ('platform', platform),
        ('rating', user_contest_record.rating),
        ('contest length', user_contest_record.length),
    )])


_plt_lock = Lock()


def get_user_contest_record_graph(user_contest_record: crawl_service_pb2.UserContestRecord) -> str:
    # 返回文件路径
    global _plt_lock
    x, y = [], []
    for record in user_contest_record.record:
        x.append(datetime.datetime.fromtimestamp(record.timestamp))
        y.append(record.rating)
    path = os.path.join(ROOT, '.tmp')
    if not os.path.exists(path):
        os.mkdir(path)
    file = os.path.join(path, f'{int(time.time())}_{random.randint(0, 998244353)}.png')
    with _plt_lock:
        plt.cla()
        plt.plot(x, y, 'go-')
        plt.xlabel('time')
        plt.ylabel('rating')
        plt.savefig(file)
    return file


def user_contest_record_card_parser(handle: str, platform: str,
                                    user_contest_record: crawl_service_pb2.UserContestRecord) -> Dict:
    colors = ('blue', 'wathet', 'turquoise', 'green', 'yellow', 'orange', 'red', 'carmine', 'violet', 'purple',
              'indigo')
    graph_path = get_user_contest_record_graph(user_contest_record)
    img_key = upload_image(graph_path)
    data = (
        ('handle', handle),
        ('platform', platform),
        ('rating', user_contest_record.rating),
        ('比赛场次', user_contest_record.length),
    )
    element = []
    for key, value in data:
        element.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"{key}： {value}",
            },
        })
    return {
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"{handle} {platform} 比赛记录",
            },
            "template": random.choice(colors),
        },
        "elements": element + [
            {
                "tag": "img",
                "img_key": img_key,
                "alt": {
                    "tag": "plain_text",
                    "content": ""
                },
            },
        ],
    }


if __name__ == '__main__':
    print(get_user_contest_record_graph(crawl_service_pb2.UserContestRecord(
        record=[
            crawl_service_pb2.UserContestRecord.Record(
                timestamp=1628957604,
                rating=200
            ),
            crawl_service_pb2.UserContestRecord.Record(
                timestamp=1528957604,
                rating=244
            ),
        ]
    )))
