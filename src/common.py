# 一些公用的方法和变量
import os, yaml, time, config

# 爬虫header
header = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

# 爬虫代理
proxy = config.GetConfig('proxy')

# 一些关于时间的常量
kSecondsPerHour = 3600
kNsPerHour = kSecondsPerHour * (10 ** 9)
kNsPerTwoHour = kNsPerHour * 2


# 获取时间戳 单位10^{-9}s
def GetTime():
    return int(time.time() * (10 ** 9))


# 不存在抛出该异常
class NoSuchUserException(Exception):
    def __init__(self, username):
        Exception.__init__(self, f'user {username} not found!')
