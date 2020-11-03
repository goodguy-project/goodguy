import requests, common, sys
from lxml import etree
from promise import Promise
from cache import Cache

header = common.header
proxy = common.proxy


def GetAtcoderRating(handle):
  global header, proxy
  try:
    html = etree.HTML(requests.get(f'https://atcoder.jp/users/{handle}', headers=header, proxies=proxy).text)
    if len(html.xpath('//*[@id="main-container"]/div[3]//h1[@class="text-center"]')) != 0:
      raise common.NoSuchUserException(handle)
    return int(html.xpath('//span[starts-with(@class, "user-")]')[1].text)
  except IndexError:
    return 0


def GetAtcoderData(handle):
  promise_rating = Promise(GetAtcoderRating, (handle,))
  promise_rating.start()
  promise_rating.join()
  data = {
    'rating': promise_rating.result
  }
  print(handle, data)
  return data


atcoder_cache = Cache(GetAtcoderData)


def GetAtcoderPromise(handle):
  return atcoder_cache.GetPromise(handle)


def AtcoderDataToString(handle, data: dict):
  return f'用户名：{handle}\nAtcoder Rating：{data["rating"]}'
