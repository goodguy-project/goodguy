import os, threading
from goodguy.util.my_promise import Promise
from apscheduler.schedulers.background import BackgroundScheduler
from goodguy.feishu.send_message import SendMessage
from goodguy.util.send_email import SendEmail
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

notice_id = set()
tmp_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notice.tmp')
notice_id_lock = threading.Lock()


# 从文件中读取数据
def LoadFromNoticeId():
  global tmp_file_path, notice_id, notice_id_lock
  if not os.path.exists(tmp_file_path):
    return
  with notice_id_lock:
    # 重置
    notice_id = set()
    # 读取数据
    with open(tmp_file_path, 'r', encoding='utf-8') as f:
      notice_ids = f.read().split(',')
      for a_notice_id in notice_ids:
        notice_id.add(a_notice_id)


# 一启动就读文件
LoadFromNoticeId()


# 异步更新到文件中 有极小概率有更新失败的情况
def UpdateNoticeId():
  global tmp_file_path, notice_id, notice_id_lock

  def UpdateNoticeIdInner():
    with notice_id_lock:
      with open(tmp_file_path, 'w', encoding='utf-8') as f:
        s = ''
        for a_notice_id in notice_id:
          if s != '':
            s += ','
          s += a_notice_id
        f.write(s)

  # 异步更新
  Promise(UpdateNoticeIdInner).start()


# 增加notice_id的api
def AddNoticeId(message_type, send_id):
  notice_id.add(message_type + "|" + send_id)
  UpdateNoticeId()


# 删除notice_id的api
def RemoveNoticeId(message_type, send_id):
  tmp = message_type + "|" + send_id
  if tmp in notice_id:
    notice_id.remove(message_type + "|" + send_id)
    UpdateNoticeId()


# 调度器 使用北京时间
scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
scheduler.start()
# 消息去重管理
msg_set = set()
msg_set_lock = threading.Lock()


def FormatAddr(s):
  name, addr = parseaddr(s)
  return formataddr((Header(name, 'utf-8').encode(), addr))


def Report(date_time, msg: str, is_send_email=True):
  global notice_id, notice_id_lock, msg_set, msg_set_lock
  msg_in_set = str(date_time) + msg
  with msg_set_lock:
    if msg_in_set not in msg_set:
      return
    msg_set.remove(msg_in_set)
  with notice_id_lock:
    for a_notice_id in notice_id:
      message_type, send_id = a_notice_id.split('|')
      SendMessage(message_type, send_id, msg)
    email_msg = MIMEText(msg.replace('\n', '\r\n'), 'plain', 'utf-8')
    email_msg['From'] = 'ConanYu <ConanYu@foxmail.com>'
    email_msg['Subject'] = '比赛邮件提醒'
    if is_send_email:
      SendEmail(email_msg)


def AddJob(date_time, msg, *args, **kwargs):
  global scheduler, msg_set, msg_set_lock
  msg_in_set = str(date_time) + msg
  is_send_email = kwargs.get('is_send_email', True)
  with msg_set_lock:
    if msg_in_set not in msg_set:
      msg_set.add(msg_in_set)
      print(msg_in_set)
      scheduler.add_job(
        Report,
        trigger='date',
        args=(date_time, msg, is_send_email),
        run_date=date_time
      )
