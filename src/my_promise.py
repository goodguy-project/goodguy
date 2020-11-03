import threading


def DoNothing(*args, **kwargs):
  pass


class Promise(threading.Thread):
  def __init__(self, func=DoNothing, argv=(), callback=DoNothing, callback_argv=()):
    super(Promise, self).__init__()
    self.func = func
    self.argv = argv
    self.callback = callback
    self.callback_argv = callback_argv

  # 重载run函数
  def run(self):
    self.result = self.func(*self.argv)
    self.callback(*self.callback_argv, self.result)
