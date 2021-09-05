import random
from typing import Dict

from goodguy.util.const import COLORS
from goodguy.util.timestamp_to_date_string import timestamp_to_date_string
from goodguy.pb import crawl_service_pb2
from goodguy.service.crawl import get_recent_contest


def recent_contest_parser(platform: str, contest: crawl_service_pb2.RecentContest) -> str:
    cts = list(contest.recent_contest)
    cts.sort(key=lambda x: x.timestamp)
    return f'{platform} recent contest:\n' + '\n'.join(
        f'name: {c.name}\nurl: {c.url}\ntime: {timestamp_to_date_string(c.timestamp)}' for c in cts)


def recent_contest_card_parser(platform: str, contest: crawl_service_pb2.RecentContest) -> Dict:
    cts = list(contest.recent_contest)
    cts.sort(key=lambda x: x.timestamp)
    element = []
    for c in cts:
        end_ts = c.timestamp + c.duration
        element.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"{timestamp_to_date_string(c.timestamp)} - {timestamp_to_date_string(end_ts)}\n"
                           f"[{c.name}]({c.url})",
            }
        })
        element.append({
            "tag": "hr",
        })
    if element:
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
            "template": random.choice(COLORS),
        },
        "elements": element,
    }


if __name__ == '__main__':
    print(recent_contest_parser('codeforces', get_recent_contest('codeforces')))
