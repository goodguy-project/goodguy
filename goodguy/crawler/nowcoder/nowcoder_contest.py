import requests, datetime
import goodguy.util.common as common
from lxml import etree
from goodguy.util.my_promise import Promise
from goodguy.util.cache import AutoCache
from goodguy.util.notice import AddJob

header = common.header
proxy = common.proxy


def GetStartTimeFromStr(msg: str) -> datetime.datetime:
  return datetime.datetime.strptime(msg[5:21], "%Y-%m-%d %H:%M")


def NoticeContestMessge(contest: dict) -> str:
  head = '如下比赛将在两小时后开始'
  name = f'名称：{contest["name"]}'
  time = f'{contest["time"]}'
  url = f'网址：{contest["url"]}'
  return '\n'.join((head, name, time, url))


def HandleElement(element: etree._Element) -> dict:
  contest = etree.HTML(etree.tostring(element))
  data = {
    "name": contest.xpath('//a')[0].text,
    "time": contest.xpath('//li[@class="match-time-icon"]')[0].text.replace('\n', ''),
    "user": contest.xpath('//li[@class="user-icon"]')[0].text,
    "url": 'https://nowcoder.com' + contest.xpath('//a/@href')[0]
  }
  data["start"] = GetStartTimeFromStr(data["time"])
  data["notice"] = data["start"] - datetime.timedelta(hours=2)
  AddJob(data["notice"], NoticeContestMessge(data), is_send_email=False)
  return data


def GetNowcoderOfficialContest() -> list:
  html = requests.get("https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=13", headers=header,
                      proxies=proxy).text
  obj = etree.HTML(html)
  contests = obj.xpath('//div[contains(@class, "js-current")]//div[@class="platform-item-cont"]')
  ret = []
  for contest in contests:
    ret.append(HandleElement(contest))
  return ret


def GetNowcoderUnofficialContest() -> list:
  html = requests.get("https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=14", headers=header,
                      proxies=proxy).text
  obj = etree.HTML(html)
  contests = obj.xpath('//div[contains(@class, "js-current")]//div[@class="platform-item-cont"]')
  ret = []
  for contest in contests:
    ret.append(HandleElement(contest))
  return ret


def GetNowcoderAllContest():
  official = Promise(GetNowcoderOfficialContest)
  unofficial = Promise(GetNowcoderUnofficialContest)
  official.start()
  unofficial.start()
  official.join()
  unofficial.join()
  result = official.result + unofficial.result
  result.sort(key=lambda item: item["time"])
  return result


nowcoder_contest_cache = AutoCache(GetNowcoderAllContest, 21600)


def NowcoderAllContestToString(contests):
  ret = '最近Nowcoder比赛：\n'
  for contest in contests:
    ret += f'比赛名称：{contest["name"]}\n'
    ret += f'{contest["time"]}\n'
    ret += f'比赛网址：{contest["url"]}\n'
    ret += f'{contest["user"]}\n\n'
  return ret[:-2]


def GetNowcoderContest():
  global nowcoder_contest_cache
  return NowcoderAllContestToString(nowcoder_contest_cache.Get())


if __name__ == "__main__":
  print(GetNowcoderAllContest())
