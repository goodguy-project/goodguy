import smtplib, time
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


# limit: 每封邮件限制人数
def SendEmail(msg: str, limit=10):
  from_addr = config.GetConfig('email', 'from')
  to_addrs = config.GetConfig('email', 'to')
  password = config.GetConfig('email', 'password')
  smtp_server = config.GetConfig('email', 'smtp', 'server')
  smtp_port = config.GetConfig('email', 'smtp', 'port')
  if to_addrs is None or to_addrs == []:
    return
  while len(to_addrs) > 0:
    mail = MIMEText(msg, 'plain', 'utf-8')
    mail['Subject'] = '比赛邮件提醒'
    mail['From'] = from_addr
    cur_to_addrs = to_addrs[:limit]
    mail['To'] = ', '.join(cur_to_addrs)
    SendEmailFunc(from_addr, cur_to_addrs, password, smtp_server, smtp_port, mail)
    to_addrs = to_addrs[limit:]
    time.sleep(config.GetConfig("email", "delay", default=61.0))
