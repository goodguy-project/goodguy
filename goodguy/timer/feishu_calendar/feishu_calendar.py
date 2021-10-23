import time
import logging
from typing import Tuple

import requests
from retrying import retry

from goodguy.feishu.access_token import get_tenant_access_token
from goodguy.service.crawl import get_recent_contest
from goodguy.util.catch_exception import catch_exception
from goodguy.util.config import GLOBAL_CONFIG
from goodguy.util.const import PLATFORM_ALL
from goodguy.util.color import rgb_to_int


def get_event_color(platform: str) -> int:
    res = GLOBAL_CONFIG.get(f'calendar.event_color.{platform}', 0)
    try:
        res = tuple(map(int, res[1:-1].split(',')))
    except Exception as e:
        logging.warning(f'bad color config of {platform}: {res}')
        return 0
    return rgb_to_int(res)

class Calendar:

    def __init__(self):
        pass
        # print(self.__token)
        # print(self.__calendar_id)

    @property
    def __token(self):
        return get_tenant_access_token()

    @property
    def __calendar_id(self):
        return GLOBAL_CONFIG.get('calendar.id')

    @catch_exception(ret=[])
    @retry(stop_max_attempt_number=5, wait_fixed=20000)
    def get_all_events(self, begin_time=0):
        events = []
        retry_time = 5
        page_token = ''
        while retry_time > 0:
            response = requests.get(
                url=f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.__calendar_id}'
                    f'/events?page_size=1000&anchor_time={str(begin_time)}&page_token={page_token}',
                headers={
                    'Authorization': f'Bearer {self.__token}',
                    'content-type': 'application/json; charset=utf-8'
                })

            if response.ok:
                response = response.json()
                if response['code'] != 0: # 正常错误码应为0
                    retry_time -= 1
                    continue
                if 'items' not in response['data']: # 日程为空
                    break
                for event in response['data']['items']:
                    if event['status'] != 'cancelled':  # 删除的 event 不会清掉，而是 status 变为 cancelled
                        events.append({
                            key: event[key]
                            for key in ['summary', 'description', 'start_time', 'end_time', 'event_id', 'color']
                        })

                if response['data']['has_more']:
                    page_token = response['data']['page_token']
                else:
                    break
            else:
                logging.debug(f'error when get url: {response.url} with status code {response.status_code}')
                retry_time -= 1
        if retry_time == 0:
            raise Exception('"get_all_events" faild after some retry')

        return events

    @retry(stop_max_attempt_number=5, wait_fixed=20000)
    def update_event(self, old_event, new_event):
        response = requests.patch(
            url=f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.__calendar_id}/events/{old_event["event_id"]}',
            headers={
                'Authorization': f'Bearer {self.__token}',
                'content-type': 'application/json; charset=utf-8'
            },
            json=new_event
        )
        logging.debug(response.text)

    @retry(stop_max_attempt_number=5, wait_fixed=20000)
    def create_event(self, new_event):
        response = requests.post(
            url=f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.__calendar_id}/events',
            headers={
                'Authorization': f'Bearer {self.__token}',
                'content-type': 'application/json; charset=utf-8'
            },
            json=new_event
        )
        logging.debug(response.text)

    @retry(stop_max_attempt_number=5, wait_fixed=20000)
    def delete_event(self, event):
        response = requests.delete(
            url=f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.__calendar_id}/events/{event["event_id"]}',
            headers={
                'Authorization': f'Bearer {self.__token}',
                'content-type': 'application/json; charset=utf-8'
            }
        )
        logging.debug(response.text)

    @retry(stop_max_attempt_number=5, wait_fixed=20000)
    def update_all_events(self):
        old_events = self.get_all_events()
        # TODO 暂且以比赛名字为唯一标识符
        old_events = {event['summary']: event for event in old_events}

        for platform in PLATFORM_ALL:
            contests = get_recent_contest(platform)
            for contest in contests.recent_contest:
                new_event = {
                    'summary': contest.name,
                    'description': f'{platform} {contest.url}',
                    'start_time': {
                        'timestamp': str(contest.timestamp),
                        'timezone': 'Asia/Shanghai'
                    },
                    'end_time': {
                        'timestamp': str(contest.timestamp + contest.duration),
                        'timezone': 'Asia/Shanghai'
                    },
                    'color': get_event_color(platform)

                }
                if contest.name in old_events:
                    print(contest.name)
                    self.update_event(old_events[contest.name], new_event)
                else:
                    self.create_event(new_event)

    # 默认保留一周内的事件
    @retry(stop_max_attempt_number=5, wait_fixed=20000)
    def delete_timeout_events(self, timeout=-60 * 60 * 24 * 7):
        old_events = self.get_all_events()
        last_time = int(time.time()) + timeout
        for event in old_events:
            if int(event['start_time']['timestamp']) < last_time:
                self.delete_event(event)


if __name__ == '__main__':
    c = Calendar()
    print(get_recent_contest('codeforces'))
    # all = c.get_all_events()
    # print(all)
    # c.delete_timeout_events(timeout=60 * 60 * 24 * 90)
    c.update_all_events()
    
