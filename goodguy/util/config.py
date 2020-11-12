import yaml, os

conf = None


def ReloadConfig():
  global conf
  dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  with open(os.path.join(dir_name, 'config.yml'), 'r', encoding='utf-8') as config_file:
    conf = yaml.load(config_file.read(), yaml.FullLoader)
  print(conf)


ReloadConfig()

"""
获取配置，如以下yaml配置文件：
```yaml
a: 1
b:
  - 2
  - 3
```
`config.GetConfig("b", 1)`会得到3
"""


def GetConfig(*args, **kwargs):
  global conf
  ret = conf
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


if __name__ == "__main__":
  print(GetConfig('app', 'id'))
