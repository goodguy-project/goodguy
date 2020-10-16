from threading import Lock, Thread
def synchronized(func):
  func.__lock__ = Lock()

  def lock_func(*args, **kwargs):
    with func.__lock__:
      return func(*args, **kwargs)

  return lock_func

class Singleton(object):
  @synchronized
  def __new__(self, *args, **kwargs):
    if Singleton._instance is None:
      Singleton._instance = super().__new__(self)
    return Singleton._instance

  _instance = None


if __name__ == "__main__":
  class NoSingleton(object):
    pass

  class TestSingleton(Singleton):
    pass
  
  class MyThread(Thread):
    def __init__(self, id):
      Thread.__init__(self)
      self.id = id
    
    def run(self):
      print(f'start thread id {self.id}\n', end='')
      TestSingleton().a = self.id
      print(f'thread id {self.id}: {TestSingleton().a}\n', end='')
      print(f'end thread id {self.id}\n', end='')

  threads = [MyThread(0), MyThread(1), MyThread(2), MyThread(3)]
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()
  NoSingleton().a = 3
  print(NoSingleton().a)