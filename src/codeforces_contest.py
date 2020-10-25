import time, requests, json, common
from promise import Promise
from cache import Cache, AutoCache

header = common.header
proxy = common.proxy


def GetCodeforcesUpcomingContestFunc(url='https://codeforces.ml/'):
    response = json.loads(requests.get(url + 'api/contest.list?gym=false', proxies=proxy, headers=header).text)
    upcoming_contest = []
    for contest in response['result']:
        if contest['phase'] == 'BEFORE':
            upcoming_contest.append(contest)
    return upcoming_contest


# 过期时间6小时
# TODO(ConanYu): 这里不应该使用Cache
upcoming_contest_cache = AutoCache(GetCodeforcesUpcomingContestFunc, 21600)

def GetCodeforcesUpcomingContest():
    return upcoming_contest_cache.Get()

def CodeforcesUpcomingContestDataToString(data):
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

    ret = '最近Codeforces比赛：\n'
    contests = data[::-1]
    for contest in contests:
        start_time = time.localtime(contest["startTimeSeconds"])
        ret += f'比赛名称: {contest["name"]}\n开始时间：{start_time.tm_year}年{start_time.tm_mon}月{start_time.tm_mday}日 {"%02d" % (start_time.tm_hour)}:{"%02d" % (start_time.tm_min)}\n比赛长度：{LengthToString(contest["durationSeconds"])}\n\n'
    return ret[:-2]
