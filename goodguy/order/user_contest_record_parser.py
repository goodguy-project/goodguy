import random
from typing import Dict

from goodguy.pb import crawl_service_pb2


def user_contest_record_parser(handle: str, platform: str,
                               user_contest_record: crawl_service_pb2.UserContestRecord) -> str:
    return "\n".join([f"{key}: {value}" for key, value in (
        ('handle', handle),
        ('platform', platform),
        ('rating', user_contest_record.rating),
        ('contest length', user_contest_record.length),
    )])


def user_contest_record_card_parser(handle: str, platform: str,
                                    user_contest_record: crawl_service_pb2.UserContestRecord) -> Dict:
    colors = ('blue', 'wathet', 'turquoise', 'green', 'yellow', 'orange', 'red', 'carmine', 'violet', 'purple',
              'indigo')
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
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": user_contest_record_parser(handle, platform, user_contest_record),
                },
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "TODO 折线图 展示",
                },
            },
        ],
    }
