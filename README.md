# GoodGuy（好家伙）

## 简介

### 飞书查询机器人

|Online Judge|作用|命令|
|----|----|----|
|Codeforces|查询用户|cf {Codeforces ID}|
|Codeforces|查询最近比赛|cf|
|Nowcoder|查询用户|nc {Nowcoder ID}|
|Nowcoder|查询最近比赛|nc|
|AtCoder|查询用户|atc {AtCoder ID}|
|AtCoder|查询最近比赛|atc|
|LeetCode|查询最近比赛|lc|
|\|给该群添加提醒|remind|
|\|取消提醒|forget|

### 邮件提醒机器人

开启邮件提醒后，当要有比赛开始时会发送比赛邮件提醒的推送。

## 使用方法

### CrawlService

爬虫基于项目 [CrawlService](https://github.com/ConanYu/CrawlService) ，需要先运行 [CrawlService](https://github.com/ConanYu/CrawlService) 再运行本项目。

### 安装Python3

建议最高版本，方法略。

### 安装Python依赖

`pip install -r requirements.txt`

### 配置PYTHONPATH

Windows: 在项目根目录下执行`set PYTHONPATH=.`
Mac Linux: 在项目根目录下执行`export PYTHONPATH=.`

### 配置文件

配置文件只有一个，为根目录下的config.yml文件。

如果需要使用飞书机器人，需要在配置文件中的feishu的进行补充信息。

如果需要使用到邮件机器人，需要在配置文件中的email的配置中进行补充信息。

如果某些功能没有生效，可以先查看一下配置文件是否配置好。

### 运行

命令行执行 `python goodguy/main.py`
