import config, common, time
from codeforces_contest import GetCodeforcesUpcomingContest
from codeforces import GetCodeforcesPromise, CodeforcesDataToString
from atcoder import GetAtcoderPromise, AtcoderDataToString

kMenu = '''1.查询用户Codeforces情况，样式：`cf 用户名`
2.查询用户Atcoder情况，样式：`atc 用户名`
3.查询Codeforces最近比赛，样式：`cf`'''


def GetFromPromise(future, expire, data_to_string_func, argv=()):
    start_time = common.GetTime()
    while not common.GetTime() - start_time > expire * 1000000000:
        time.sleep(float(0.01))
    if hasattr(future, 'result'):
        return data_to_string_func(*argv, future.result)
    return None


def Converse(text: str) -> str:
    global kMenu
    result = None
    text_split = text.split()
    f = '' if len(text_split) <= 0 else text_split[0]
    handle = '' if len(text_split) <= 1 else text_split[1]
    f = f.lower()
    # 查询菜单
    if f in {'菜单', 'menu', ''}:
        result = kMenu
    # 重载配置文件（一般不使用）
    elif f == 'reload_config':
        config.ReloadConfig()
        result = 'Reload Config OK'
        print('reload config successd.')
    # 查询Codeforces信息
    elif f in {'cf', 'codeforces'}:
        # 查询Codeforces最近比赛
        if handle == '':
            result = GetCodeforcesUpcomingContest()
        # 查询Codeforces用户
        else:
            result = GetFromPromise(GetCodeforcesPromise(handle.lower()), 15.0, CodeforcesDataToString, (handle,))
    # 查询Atcoder信息
    elif f in {'atc', 'atcoder'}:
        result = GetFromPromise(GetAtcoderPromise(handle.lower()), 15.0, AtcoderDataToString, (handle,))
    # 未知输入
    if result is None:
        result = f'命令 {text} 发生未知错误，用法：\n{kMenu}'
    return result

if __name__ == "__main__":
    print(Converse(input()))