import requests, datetime, json, time
import goodguy.util.common as common
from goodguy.util.cache import AutoCache
from goodguy.util.notice import AddJob

proxy = common.proxy
header = common.header


# 比赛时长（单位：秒）转换成字符串
def LengthToString(length):
  day = length // 86400
  hour = str(length % 86400 // 3600)
  minute = str(length % 3600 // 60)
  while len(hour) < 2:
    hour = '0' + hour
  while len(minute) < 2:
    minute = '0' + minute
  ret_str = ''
  if day != 0:
    ret_str += f'{day}:'
  ret_str += f'{hour}:{minute}'
  return ret_str


# Contest转换成消息字符串
def NoticeContestMessge(contest):
  head = '如下比赛将在两小时后开始'
  name = f'名称：{contest["title"]}'
  start_time = time.localtime(contest["start_time"].timestamp())
  when = f'时间：{start_time.tm_year}年{start_time.tm_mon}月{start_time.tm_mday}日 {"%02d" % (start_time.tm_hour)}:{"%02d" % (start_time.tm_min)}（北京时间）'
  duration = f'时长：{LengthToString(contest["duration"])}'
  url = f'网址：https://leetcode-cn.com/contest/'
  return '\n'.join((head, name, when, duration, url))


def LeetcodeContestDataToString(contests):
  ret = '最近Leetcode比赛：\n'
  for contest in contests:
    start_time = time.localtime(contest["start_time"].timestamp())
    ret += f'比赛名称: {contest["title"]}\n比赛时间：{start_time.tm_year}年{start_time.tm_mon}月{start_time.tm_mday}日 {"%02d" % (start_time.tm_hour)}:{"%02d" % (start_time.tm_min)}\n比赛时长：{LengthToString(contest["duration"])}\n\n'
  return ret[:-2]


def GetLeetcodeUpcomingContestFunc() -> dict:
  global header, proxy
  session = requests.Session()
  data = json.dumps({
    "operationName": None,
    "variables": dict(),
    "query": "{\n  brightTitle\n  contestUpcomingContests {\n    containsPremium\n    title\n    cardImg\n    titleSlug\n    description\n    startTime\n    duration\n    originStartTime\n    isVirtual\n    company {\n      watermark\n      __typename\n    }\n    __typename\n  }\n}\n"
  }).encode('utf-8')
  cookies = session.get('https://leetcode-cn.com/contest/', headers=header, proxies=proxy).cookies
  csrftoken = None
  for cookie in cookies:
    if cookie.name == 'csrftoken':
      csrftoken = cookie.value
  cur_header = header.copy()
  cur_header['x-csrftoken'] = csrftoken
  cur_header['origin'] = 'https://leetcode-cn.com'
  cur_header['referer'] = 'https://leetcode-cn.com/contest/'
  cur_header['Connection'] = 'keep-alive'
  cur_header['Content-Type'] = 'application/json'
  result = session.post('https://leetcode-cn.com/graphql', data=data, headers=cur_header, proxies=proxy).json()['data']['contestUpcomingContests']
  ret = []
  for contest in result:
    start_time = datetime.datetime.fromtimestamp(contest['startTime'])
    duration = contest['duration']
    title = contest['title']
    item = {
      'start_time': start_time,
      'duration': duration,
      'title': title
    }
    ret.append(item)
    # 提前两小时提醒
    AddJob(start_time - datetime.timedelta(hours=2), NoticeContestMessge(item))
  return ret


upcoming_contest_cache = AutoCache(GetLeetcodeUpcomingContestFunc, 21600)


def GetLeetcodeUpcomingContest():
  global upcoming_contest_cache
  return LeetcodeContestDataToString(upcoming_contest_cache.Get())
  

if __name__ == "__main__":
  print(LeetcodeContestDataToString(GetLeetcodeUpcomingContestFunc()))