import yaml
from singleton import Singleton

class Config(Singleton):
  # 配置初始化 不执行就没有数据
  def Init(self):
    self.ReloadConfig()

  # 配置热更新
  def ReloadConfig(self):
    with open('../config.yml', 'r', encoding='utf-8') as config_file:
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
  def GetConfig(self, *args):
    ret = self.config
    for arg in args:
      if ret is None:
        return None
      if isinstance(ret, dict):
        ret = ret.get(arg, None)
      else:
        ret = ret[arg]
    return ret

# 单元测试
if __name__ == "__main__":
  Config().Init()
  print(Config().GetConfig("b"))