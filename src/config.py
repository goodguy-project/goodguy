import yaml, os
from singleton import Singleton

class Config(Singleton):
  # 配置初始化 不执行就没有数据
  def Init(self):
    self.ReloadConfig()

  # 配置热更新
  def ReloadConfig(self):
    dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(dir_name, 'config.yml'), 'r', encoding='utf-8') as config_file:
      self.config = yaml.load(config_file.read(), yaml.FullLoader)

  """
  获取配置，如以下yaml配置文件：
  ```yaml
  a: 1
  b:
    - 2
    - 3
  ```
  `Config().GetConfig("b", 1)`会得到3
  """
  def GetConfig(self, *args, **kwargs):
    ret = self.config
    for arg in args:
      if ret is None:
        return kwargs.get("default", None)
      try:
        ret = ret[arg]
      except Exception:
        ret = None
        pass
      if ret is None:
        return kwargs.get("default", None)
    return ret

# 单元测试
if __name__ == "__main__":
  Config().Init()
  print(Config().GetConfig("app.verification.token"))