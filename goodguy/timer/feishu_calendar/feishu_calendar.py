import requests
import time

from goodguy.feishu.access_token import get_tenant_access_token
from goodguy.service.crawl import get_recent_contest
from goodguy.util.config import GLOBAL_CONFIG
from goodguy.util.platform_all import PLATFORM_ALL


class Calendar():

    def __init__(self):
        print(self.__token)
        print(self.__calendar_id)

    @property
    def __token(self):
        return get_tenant_access_token()

    @property
    def __calendar_id(self):
        return GLOBAL_CONFIG.get('calendar.id')

    # TODO 日程太多时会分页，应改为逐页获取，默认一页有 500 个，虽然理论上不会有 500 个 event
    def get_all_events(self, begin_time=0):
        events = []
        # 获取过程有 retry_time 次网络问题则 gg，每次获取失败重新获取当前页
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
                response = response.json()['data']
                for event in response['items']:
                    if event['status'] != 'cancelled':  # 删除的 event 不会清掉，而是 status 变为 cancelled
                        events.append({
                            key: event[key]
                            for key in ['summary', 'description', 'start_time', 'end_time', 'event_id']
                        })

                if response['has_more']:
                    page_token = response['page_token']
                else:
                    break
            else:
                retry_time -= 1

        return events

    def update_event(self, old_event, new_event):
        response = requests.patch(
            url=f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.__calendar_id}/events/{old_event["event_id"]}',
            headers={
                'Authorization': f'Bearer {self.__token}',
                'content-type': 'application/json; charset=utf-8'
            },
            json=new_event
        )

    def create_event(self, new_event):
        response = requests.post(
            url=f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.__calendar_id}/events',
            headers={
                'Authorization': f'Bearer {self.__token}',
                'content-type': 'application/json; charset=utf-8'
            },
            json=new_event
        )

    def delete_event(self, event):
        response = requests.delete(
            url=f'https://open.feishu.cn/open-apis/calendar/v4/calendars/{self.__calendar_id}/events/{event["event_id"]}',
            headers={
                'Authorization': f'Bearer {self.__token}',
                'content-type': 'application/json; charset=utf-8'
            }
        )

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

                }
                if contest.name in old_events:
                    self.update_event(old_events[contest.name], new_event)
                else:
                    self.create_event(new_event)

    # 默认保留一周内的事件
    def delete_timeout_events(self, timeout=60 * 60 * 24 * 7):
        old_events = self.get_all_events()
        last_time = int(time.time()) - timeout
        for event in old_events:
            if int(event['start_time']['timestamp']) < last_time:
                self.delete_event(event)


if __name__ == '__main__':
    c = Calendar()
    c.delete_timeout_events(timeout=60 * 60 * 24 * 3)
