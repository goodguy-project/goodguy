import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PLATFORM_ALL = ['codeforces', 'nowcoder', 'atcoder', 'leetcode', 'luogu']

USAGE = '''1.查询用户CodeForces情况，样式：`cf 用户名`
2.查询用户AtCoder情况，样式：`atc 用户名`
3.查询CodeForces最近比赛，样式：`cf`
4.给该群添加提醒，样式：`remind`
5.取消提醒，样式：`forget`
6.查询NowCoder情况，样式：`nc 牛客ID`
7.查询NowCoder最近比赛，样式：`nc`
8.查询AtCoder最近比赛，样式：`atc`
9.查询LeetCode最近比赛，样式：`lc`'''

COLORS = ('blue', 'wathet', 'turquoise', 'green', 'yellow', 'orange', 'red', 'carmine', 'violet', 'purple', 'indigo')

if __name__ == '__main__':
    print(locals())
