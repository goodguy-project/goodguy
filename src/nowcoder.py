# 牛客爬虫 仅支持牛客id（纯数字）
import requests, common, json
from promise import Promise
from lxml import etree
from cache import Cache
from promise import Promise

header = common.header
proxy = common.proxy


def GetNowcoderACMData(handle):
  global header, proxy
  url = f'https://ac.nowcoder.com/acm/contest/profile/{handle}'
  response = requests.get(url, headers=header, proxies=proxy)
  obj = etree.HTML(response.text)
  tmp = obj.xpath('//div[contains(@class, "state-num")]')
  if len(tmp) < 4:
    raise common.NoSuchUserException(handle)
  rating = tmp[0].text
  rating_rank = tmp[1].text
  contest_cnt = tmp[3].text
  return {
    'rating': rating,
    'rating_rank': rating_rank,
    'contest_cnt': contest_cnt
  }


def GetNowcoderProfile(handle):
  global header, proxy
  url = f'https://www.nowcoder.com/profile/{handle}'
  response = requests.get(url, headers=header, proxies=proxy)
  obj = etree.HTML(response.text)
  tmp1 = obj.xpath('//span[@class="txt"]')
  tmp2 = obj.xpath('//span[@class="num"]')
  if len(tmp1) < 1 or len(tmp2) < 3:
    raise common.NoSuchUserException(handle)
  achievement = tmp1[0].text
  like = tmp2[0].text
  correct = tmp2[1].text
  accepted = tmp2[2].text
  return {
    'achievement': achievement,
    'like': like,
    'correct': correct,
    'accepted': accepted
  }


def GetNowcoderData(handle):
  promise_acm = Promise(GetNowcoderACMData, (handle,))
  promise_profile = Promise(GetNowcoderProfile, (handle,))
  promise_acm.start()
  promise_profile.start()
  promise_acm.join()
  promise_profile.join()
  print(handle, promise_acm.result, promise_profile.result)
  return {
    'acm': promise_acm.result,
    'profile': promise_profile.result
  }

nowcoder_cache = Cache(GetNowcoderData)


def NowcoderDataToString(handle, data):
  rating      = data['acm']['rating']
  rating_rank = data['acm']['rating_rank']
  contest_cnt = data['acm']['contest_cnt']
  achievement = data['profile']['achievement']
  like        = data['profile']['like']
  correct     = data['profile']['correct']
  accepted    = data['profile']['accepted']
  return f'牛客ID：{handle}\n\n牛客竞赛\nRating：{rating}\nRating排名：{rating_rank}\n参加过比赛次数：{contest_cnt}\n\n牛客主站\n成就值：{achievement}\n获赞与收藏：{like}\n题目正确：{correct}\n编程正确：{accepted}'


def GetNowcoderPromise(handle):
  return nowcoder_cache.GetPromise(handle)

if __name__ == "__main__":
  print(NowcoderDataToString(6693394, GetNowcoderData(6693394)))
