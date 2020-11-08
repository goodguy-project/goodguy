import requests
import goodguy.util.common as common
from lxml import etree
from goodguy.util.cache import AutoCache

header = common.header
proxy = common.proxy


def GetNowcoderPopularFunc():
  html = requests.get('https://www.nowcoder.com/discuss', headers=header, proxies=proxy).text
  obj = etree.HTML(html)
  head = obj.xpath('//div[@class="nk-bar"]/div[2]//li//div[@class="list-title"]//a')
  href = obj.xpath('//div[@class="nk-bar"]/div[2]//li//div[@class="list-title"]//a/@href')
  if len(head) < 10 or len(href) < 10:
    return None
  ret = []
  for i in range(10):
    ret.append({
      "name": head[i].text,
      "url": "https://nowcoder.com" + href[i]
    })
  return ret


# 一小时更新一次
nowcoder_popular_cache = AutoCache(GetNowcoderPopularFunc, 3600)


def GetNowcoderPopular():
  global nowcoder_popular_cache
  nowcoder_popular = nowcoder_popular_cache.Get()
  ret = '牛客最近热帖：\n'
  for popular in nowcoder_popular:
    ret += f'标题：{popular["name"]}\n'
    ret += f'链接：{popular["url"]}\n\n'
  return ret[:-2]


if __name__ == "__main__":
  print(GetNowcoderPopular())
