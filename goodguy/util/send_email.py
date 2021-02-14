import smtplib
import time
import re
import goodguy.util.config as config
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.text import MIMEText


def FormatAddr(s):
  name, addr = parseaddr(s)
  return formataddr((Header(name, 'utf-8').encode(), addr))


def SendEmailFunc(from_addr, to_addrs: list, password, smtp_server, smtp_port, msg):
  server = smtplib.SMTP_SSL(smtp_server, smtp_port)
  server.login(from_addr, password)
  server.sendmail(from_addr, to_addrs, msg.as_string())
  server.quit()


def handle_competition_message(msg: str) -> str:
  msg = msg.replace('名称：', '<b>名称：</b>')
  msg = msg.replace('时间：', '<b>时间：</b>')
  msg = msg.replace('时长：', '<b>时长：</b>')
  msg: list = msg.split('\r\n')
  for index, what in enumerate(msg):
    result = re.search('http.*$', what)
    if result is not None:
      span = result.span()
      msg[index] = f'<a href="{what[span[0]:span[1]]}">比赛链接</a>'
  return f'''
  <html>
  <body>
    <style type="text/css">
      a:link {{
        color: rgb(0, 132, 255);
        text-decoration: none;
        font-weight: bold;
      }}
      a:hover {{
        text-decoration: underline;
      }}
      a:visited {{
        color: rgb(0, 132, 255);
        text-decoration: none;
      }}
    </style>
    hello, send by <a href="https://github.com/ConanYu/GoodGuy">ConanYu/GoodGuy</a>.<br>
    {'<br>'.join(msg)}<br><br>
    邮件发送时间戳：{int(time.time())}<br>
  </body>
  </html>'''


# limit: 每封邮件限制人数
def SendEmail(msg: str, limit=10):
  from_addr = config.GetConfig('email', 'from')
  to_addrs = config.GetConfig('email', 'to')
  password = config.GetConfig('email', 'password')
  smtp_server = config.GetConfig('email', 'smtp', 'server')
  smtp_port = config.GetConfig('email', 'smtp', 'port')
  if to_addrs is None or to_addrs == []:
    return
  msg = handle_competition_message(msg)
  while len(to_addrs) > 0:
    mail = MIMEText(msg, 'html', 'utf-8')
    mail['Subject'] = '比赛邮件提醒'
    mail['From'] = from_addr
    cur_to_addrs = to_addrs[:limit]
    mail['To'] = ', '.join(cur_to_addrs)
    SendEmailFunc(from_addr, cur_to_addrs, password, smtp_server, smtp_port, mail)
    to_addrs = to_addrs[limit:]
    time.sleep(config.GetConfig("email", "delay", default=61.0))
