import threading
class Promise(threading.Thread):
  def __init__(self, func=None, argv=(), callback=None, callback_argv=()):
    super(Promise, self).__init__()
    self.func = func
    self.argv = argv
    self.callback = callback
    self.callback_argv = callback_argv

  def run(self):
    self.result = self.func(*self.argv)
    if self.callback is not None:
      self.callback(*self.callback_argv, self.result)