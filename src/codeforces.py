import requests, json, common, sys, threading
from cache import Cache
from promise import Promise

header = common.header
proxy = common.proxy

# 通过handle获取Codeforces做题数
def GetCodeforcesCount(handle, url='https://codeforces.ml/'):
  global header, proxy
  response = requests.get(f'{url}api/user.status?handle={handle}', proxies=proxy, headers=header)
  response = json.loads(response.text)
  if response['status'] != 'OK':
    raise common.NoSuchUserException(handle)
  response = response['result']
  ProSet = set()
  for ele in response:
    try:
      problem = ele['problem']
      problem = str(problem['contestId']) + problem['index']
      if ele['verdict'] == 'OK':
        ProSet.add(problem)
    except Exception:
      pass
  return len(ProSet)

# 通过handle获取Codeforces Rating
def GetCodeforcesRating(handle, url='https://codeforces.ml/'):
  global header, proxy
  response = requests.get(f'{url}api/user.rating?handle={handle}', proxies=proxy, headers=header)
  response = json.loads(response.text)
  if response['status'] != 'OK':
    raise common.NoSuchUserException(handle)
  try:
    return response['result'][-1]['newRating']
  except IndexError:
    return 0

def GetCodeforcesData(handle, url='https://codeforces.ml/'):
  promise_count = Promise(GetCodeforcesCount, (handle, url))
  promise_rating = Promise(GetCodeforcesRating, (handle, url))
  promise_count.start()
  promise_rating.start()
  promise_count.join()
  promise_rating.join()
  data = {
    'count': promise_count.result,
    'rating': promise_rating.result
  }
  print(handle, data)
  return data

# 缓存
codeforces_cache = Cache(GetCodeforcesData)

def GetCodeforcesPromise(handle):
  return codeforces_cache.GetPromise(handle)

def CodeforcesDataToString(handle, data: dict):
  return f'用户名：{handle}\nCodeforces Rating：{data["rating"]}\nCodeforces做题数：{data["count"]}'
