from goodguy.order.timestamp_to_date_string import timestamp_to_date_string
from goodguy.pb import crawl_service_pb2
from goodguy.service.crawl import get_recent_contest


def recent_contest_parser(platform: str, contest: crawl_service_pb2.RecentContest) -> str:
    res = f'{platform} recent contest:\n'
    for contest in contest.recent_contest:
        res += f'name: {contest.name}\n'
        res += f'url: {contest.url}\n'
        res += f'time: {timestamp_to_date_string(contest.timestamp)}'
    return res


if __name__ == '__main__':
    print(recent_contest_parser('codeforces', get_recent_contest('codeforces')))
