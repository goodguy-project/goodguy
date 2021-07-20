import random
from typing import Dict

from goodguy.order.timestamp_to_date_string import timestamp_to_date_string
from goodguy.pb import crawl_service_pb2
from goodguy.service.crawl import get_recent_contest


def recent_contest_parser(platform: str, contest: crawl_service_pb2.RecentContest) -> str:
    return f'{platform} recent contest:\n' + '\n'.join(
        f'name: {c.name}\nurl: {c.url}\ntime: {timestamp_to_date_string(c.timestamp)}' for c in
        contest.recent_contest[::-1])


def recent_contest_card_parser(platform: str, contest: crawl_service_pb2.RecentContest) -> Dict:
    element = []
    colors = ('blue', 'wathet', 'turquoise', 'green', 'yellow', 'orange', 'red', 'carmine', 'violet', 'purple',
              'indigo')
    for c in contest.recent_contest[::-1]:
        element.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"{timestamp_to_date_string(c.timestamp)} [{c.name}]({c.url})",
            }
        })
        element.append({
            "tag": "hr",
        })
    if len(element):
        element.pop()
    return {
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"{platform} 比赛",
            },
            "template": random.choice(colors),
        },
        "elements": element,
    }


if __name__ == '__main__':
    print(recent_contest_parser('codeforces', get_recent_contest('codeforces')))
