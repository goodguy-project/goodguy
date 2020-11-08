import time
import goodguy.util.config as config
import goodguy.util.common as common
import goodguy.util.notice as notice
from goodguy.crawler.codeforces.codeforces_contest import GetCodeforcesUpcomingContest
from goodguy.crawler.codeforces.codeforces import GetCodeforcesPromise, CodeforcesDataToString
from goodguy.crawler.atcoder.atcoder import GetAtcoderPromise, AtcoderDataToString
from goodguy.crawler.atcoder.atcoder_contest import GetAtcoderContest
from goodguy.crawler.nowcoder.nowcoder import GetNowcoderPromise, NowcoderDataToString
from goodguy.crawler.nowcoder.nowcoder_contest import GetNowcoderContest
from goodguy.crawler.nowcoder.nowcoder_popular import GetNowcoderPopular

kMenu = '''1.查询用户Codeforces情况，样式：`cf 用户名`
2.查询用户Atcoder情况，样式：`atc 用户名`
3.查询Codeforces最近比赛，样式：`cf`
4.给该群添加提醒，样式：`notice`
5.取消提醒，样式：`unnotice`
6.查询Nowcoder情况，样式：`nc 牛客ID`
7.查询Nowcoder最近比赛，样式：`nc`
8.查询Atcoder最近比赛，样式：`atc`
9.查询Nowcoder最近热帖，样式：`ncp`'''


def GetFromPromise(future, expire, data_to_string_func, argv=()):
  start_time = common.GetTime()
  while not common.GetTime() - start_time > expire * 1000000000 and not hasattr(future, 'result'):
    time.sleep(float(0.01))
  if hasattr(future, 'result'):
    return data_to_string_func(*argv, future.result)
  return None


def Converse(text: str, **kwargs) -> str:
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
  # 查询AtCoder信息
  elif f in {'atc', 'atcoder'}:
    # 查询AtCoder最近比赛
    if handle == '':
      result = GetAtcoderContest()
    # 查询AtCoder用户分数
    else:
      result = GetFromPromise(GetAtcoderPromise(handle.lower()), 15.0, AtcoderDataToString, (handle,))
  # 用于Debug
  elif f == 'print_message':
    result = f'message_type: {kwargs["message_type"]}\nsend_id: {kwargs["send_id"]}'
  # 消息提醒该群聊或用户
  elif f == 'notice':
    notice.AddNoticeId(kwargs["message_type"], kwargs["send_id"])
    result = 'notice ok'
  # 取消提醒
  elif f == 'unnotice':
    notice.RemoveNoticeId(kwargs["message_type"], kwargs["send_id"])
    result = 'remove notice ok'
  # 查询NowCoder信息
  elif f in {'nc', 'nowcoder'}:
    # 查询NowCoder最近比赛
    if handle == '':
      result = GetNowcoderContest()
    # 查询NowCoder用户
    else:
      result = GetFromPromise(GetNowcoderPromise(handle), 15.0, NowcoderDataToString, (handle,))
  # 查询牛客网热榜
  elif f in {'ncp', 'nowcoder_popular'}:
    result = GetNowcoderPopular()
  # 未知输入
  if result is None:
    result = f'命令 {text} 发生未知错误，用法：\n{kMenu}'
  return result


if __name__ == "__main__":
  print(Converse(input()))
