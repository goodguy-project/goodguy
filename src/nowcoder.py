# 牛客爬虫 仅支持牛客id（纯数字）
import requests, common, json
from promise import Promise
from lxml import etree
from cache import Cache
from promise import Promise

header = common.header
proxy = common.proxy


def GetNowcoderACMData1(handle):
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


def GetNowcoderACMData2(handle):
  global header, proxy
  url = f'https://ac.nowcoder.com/acm/contest/profile/{handle}/practice-coding'
  response = requests.get(url, headers=header, proxies=proxy)
  obj = etree.HTML(response.text)
  tmp = obj.xpath('//div[@class="state-num"]')
  accepted = tmp[1].text
  submit_cnt = tmp[2].text
  return {
    'accepted': accepted,
    'submit_cnt': submit_cnt
  }


def GetNowcoderProfile(handle):
  global header, proxy
  url = f'https://www.nowcoder.com/profile/{handle}'
  response = requests.get(url, headers=header, proxies=proxy)
  obj = etree.HTML(response.text)
  name = obj.xpath('//a[contains(@class, "profile-user-name")]')
  tmp1 = obj.xpath('//span[@class="txt"]')
  tmp2 = obj.xpath('//span[@class="num"]')
  if len(tmp1) < 1 or len(tmp2) < 3 or len(name) < 1:
    raise common.NoSuchUserException(handle)
  name = name[0].get('data-title')
  achievement = tmp1[0].text
  like = tmp2[0].text
  correct = tmp2[1].text
  accepted = tmp2[2].text
  return {
    'name': name,
    'achievement': achievement,
    'like': like,
    'correct': correct,
    'accepted': accepted
  }


def GetNowcoderData(handle):
  promise_acm1 = Promise(GetNowcoderACMData1, (handle,))
  promise_acm2 = Promise(GetNowcoderACMData2, (handle,))
  promise_profile = Promise(GetNowcoderProfile, (handle,))
  promise_acm1.start()
  promise_acm2.start()
  promise_profile.start()
  promise_acm1.join()
  promise_acm2.join()
  promise_profile.join()
  print(handle, promise_acm1.result, promise_profile.result)
  return {
    'acm1': promise_acm1.result,
    'acm2': promise_acm2.result,
    'profile': promise_profile.result
  }

nowcoder_cache = Cache(GetNowcoderData)


def NowcoderDataToString(handle, data):
  rating      = data['acm1']['rating']
  rating_rank = data['acm1']['rating_rank']
  contest_cnt = data['acm1']['contest_cnt']
  accepted_c  = data['acm2']['accepted']
  submit_cnt  = data['acm2']['submit_cnt']
  name        = data['profile']['name']
  achievement = data['profile']['achievement']
  like        = data['profile']['like']
  correct     = data['profile']['correct']
  accepted    = data['profile']['accepted']
  return f'牛客ID：{handle}\n牛客用户名：{name}\n\n牛客竞赛\nRating：{rating}\nRating排名：{rating_rank}\n题目通过数：{accepted_c}\n总提交次数：{submit_cnt}\n参加过比赛次数：{contest_cnt}\n\n牛客主站\n成就值：{achievement}\n获赞与收藏：{like}\n题目正确：{correct}\n编程正确：{accepted}'


def GetNowcoderPromise(handle):
  return nowcoder_cache.GetPromise(handle)

if __name__ == "__main__":
  print(NowcoderDataToString(6693394, GetNowcoderData(6693394)))
