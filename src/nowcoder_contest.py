import requests, common, datetime
from promise import Promise
from lxml import etree

header = common.header
proxy = common.proxy


def GetStartTimeFromStr(msg: str) -> datetime.datetime:
  return datetime.datetime.strptime(msg[5:21], "%Y-%m-%d %H:%M")


def HandleElement(element: etree._Element) -> dict:
  contest = etree.HTML(etree.tostring(element))
  data = {
    "name": contest.xpath('//a')[0].text,
    "time": contest.xpath('//li[@class="match-time-icon"]')[0].text.replace('\n', ''),
    "user": contest.xpath('//li[@class="user-icon"]')[0].text
  }
  data["start"] = GetStartTimeFromStr(data["time"])
  data["notice"] = data["start"] - datetime.timedelta(hours=2)
  return data


def GetNowcoderOfficialContest() -> list:
  html = requests.get("https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=13", headers=header, proxies=proxy).text
  obj = etree.HTML(html)
  contests = obj.xpath('//div[contains(@class, "js-current")]//div[@class="platform-item-cont"]')
  ret = []
  for contest in contests:
    ret.append(HandleElement(contest))
  return ret


def GetNowcoderUnofficialContest() -> list:
  html = requests.get("https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=14", headers=header, proxies=proxy).text
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


if __name__ == "__main__":
  print(GetNowcoderAllContest())