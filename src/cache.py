# 缓存
import threading, common, config, time
from promise import Promise


class Cache(object):
  # 初始化，func为GetPromise的函数，expire为过期时间（单位s，默认为两小时）
  def __init__(self, func, expire=7200):
    self.func = func
    # 正在进行作业的用户哈希表，key为handle，value为promise
    self.crawling_map = dict()
    # 该集合的多线程锁
    self.crawling_map_lock = threading.Lock()
    # 查询结果的缓存
    self.data_map = dict()
    # 缓存的多线程锁
    self.data_map_lock = threading.Lock()
    self.expire = expire * (10 ** 9)

  def GetPromise(self, handle):
    ret = None
    # 查看在缓存中是否有数据
    with self.data_map_lock:
      data = self.data_map.get(handle, None)
      is_expire = False
      if data is not None:
        ret = Promise()
        ret.start()
        ret.result = data
        # 查看数据是否已经过期
        if data.get('crawl_time', 0) + self.expire >= common.GetTime():
          is_expire = True
    # 缓存中有数据
    if ret is not None:
      # 已经过期了
      if is_expire:
        with self.crawling_map_lock:
          # 不在爬取作业中
          if handle not in self.crawling_map:
            new_promise = Promise(self.func, (handle,), self.UpdateData, (handle,))
            new_promise.start()
            self.crawling_map[handle] = new_promise
      # 返回缓存中的数据
      return ret
    with self.crawling_map_lock:
      ret = self.crawling_map.get(handle, None)
      # 不在爬取作业中
      if ret is None:
        ret = Promise(self.func, (handle,), self.UpdateData, (handle,))
        ret.start()
        self.crawling_map[handle] = ret
    return ret

  def UpdateData(self, handle, data):
    # 更新数据
    with self.data_map_lock:
      data['crawl_time'] = common.GetTime()
      self.data_map[handle] = data
      # 数据太多了直接清完所有缓存
      if len(self.data_map) >= config.GetConfig('cache', 'maxsize', default=10000):
        self.data_map.clear()
    # 更新这个handle的状态为不是正在进行作业
    with self.crawling_map_lock:
      self.crawling_map.pop(handle)
    print(handle, data)


class AutoCache(object):
  class InnerThread(threading.Thread):
    def __init__(self, obj):
      super(AutoCache.InnerThread, self).__init__()
      self.obj = obj

    def run(self):
      while True:
        time.sleep(self.obj.expire)
        data = self.obj.func()
        with self.obj.data_lock:
          self.obj.data = data

  def __init__(self, func, expire):
    self.func = func
    self.expire = expire
    self.data_lock = threading.Lock()
    self.data = self.func()
    self.thread = AutoCache.InnerThread(self)
    self.thread.start()

  def Get(self):
    data = None
    with self.data_lock:
      data = self.data
    return data
