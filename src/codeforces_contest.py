import time, requests, json, common, datetime
from promise import Promise
from cache import Cache, AutoCache
from notice import AddJob

header = common.header
proxy = common.proxy


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
    name = f'名称：{contest["name"]}'
    start_time = time.localtime(contest["startTimeSeconds"])
    when = f'时间：{start_time.tm_year}年{start_time.tm_mon}月{start_time.tm_mday}日 {"%02d" % (start_time.tm_hour)}:{"%02d" % (start_time.tm_min)}（北京时间）'
    duration = f'时长：{LengthToString(contest["durationSeconds"])}'
    url = f'网址：https://codeforces.com/contests'
    return '\n'.join((head, name, when, duration, url))


def GetCodeforcesUpcomingContestFunc(url='https://codeforces.ml/'):
    response = json.loads(requests.get(url + 'api/contest.list?gym=false', proxies=proxy, headers=header).text)
    upcoming_contest = []
    for contest in response['result']:
        if contest['phase'] == 'BEFORE':
            upcoming_contest.append(contest)
            # 提前两个小时提醒
            start_datetime = datetime.datetime.fromtimestamp(contest['startTimeSeconds'])
            notice_datetime = start_datetime - datetime.timedelta(hours=2)
            AddJob(notice_datetime, NoticeContestMessge(contest))
    return upcoming_contest


# 过期时间6小时
upcoming_contest_cache = AutoCache(GetCodeforcesUpcomingContestFunc, 21600)


def CodeforcesUpcomingContestDataToString(data):
    ret = '最近Codeforces比赛：\n'
    contests = data[::-1]
    if len(contests) > 5:
        contests = contests[:5]
    for contest in contests:
        start_time = time.localtime(contest["startTimeSeconds"])
        ret += f'比赛名称: {contest["name"]}\n比赛时间：{start_time.tm_year}年{start_time.tm_mon}月{start_time.tm_mday}日 {"%02d" % (start_time.tm_hour)}:{"%02d" % (start_time.tm_min)}\n比赛时长：{LengthToString(contest["durationSeconds"])}\n\n'
    return ret[:-2]


def GetCodeforcesUpcomingContest():
    return CodeforcesUpcomingContestDataToString(upcoming_contest_cache.Get())