import requests, datetime
import goodguy.util.common as common
from lxml import etree
from goodguy.util.notice import AddJob
from goodguy.util.cache import AutoCache

header = common.header
proxy = common.proxy


def NoticeContestMessge(contest: dict) -> str:
  head = '如下比赛将在两小时后开始'
  name = f'名称：{contest["name"]}'
  start = contest["start"]
  time = f'时间：{start.year}年{start.month}月{start.day}日 {"%02d" % (start.hour)}:{"%02d" % (start.minute)}（北京时间）'
  url = f'网址：{contest["url"]}'
  return '\n'.join((head, name, time, url))


def GetAtcoderContestFunc() -> dict:
  html = requests.get('https://atcoder.jp/?lang=en', headers=header, proxies=proxy).text
  obj = etree.HTML(html)
  start_times = obj.xpath('//div[@id="contest-table-upcoming"]//tbody//a[@target="blank"]/time')
  contests = obj.xpath('//div[@id="contest-table-upcoming"]//tbody//a[name(@target)!="target"]')
  urls = obj.xpath('//div[@id="contest-table-upcoming"]//tbody//a[name(@target)!="target"]/@href')
  length = len(start_times)
  ret = []
  for idx in range(length):
    start = datetime.datetime.strptime(start_times[idx].text, "%Y-%m-%d %H:%M:%S%z").timestamp()
    start = datetime.datetime.fromtimestamp(start)
    data = {
      "start": start,
      "name": contests[idx].text,
      "url": "https://atcoder.jp" + urls[idx]
    }
    ret.append(data)
    AddJob(start - datetime.timedelta(hours=2), NoticeContestMessge(data))
  return ret


atcoder_contest_cache = AutoCache(GetAtcoderContestFunc, 21600)


def AtcoderContestToString(contests: list) -> str:
  ret = '最近Atcoder比赛：\n'
  for contest in contests:
    ret += f'比赛名称：{contest["name"]}\n'
    start = contest["start"]
    ret += f'比赛时间：{start.year}年{start.month}月{start.day}日 {"%02d" % (start.hour)}:{"%02d" % (start.minute)}（北京时间）\n'
    ret += f'比赛网址：{contest["url"]}\n\n'
  return ret[:-2]


def GetAtcoderContest() -> str:
  global atcoder_contest_cache
  return AtcoderContestToString(atcoder_contest_cache.Get())


if __name__ == "__main__":
  print(AtcoderContestToString(GetAtcoderContestFunc()))
