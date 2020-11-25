import smtplib
import goodguy.util.config as config
from email.header import Header
from email.utils import parseaddr, formataddr


def FormatAddr(s):
  name, addr = parseaddr(s)
  return formataddr((Header(name, 'utf-8').encode(), addr))


def SendEmailFunc(from_addr, to_addrs: list, password, smtp_server, smtp_port, msg):
  server = smtplib.SMTP_SSL(smtp_server, smtp_port)
  server.login(from_addr, password)
  server.sendmail(from_addr, to_addrs, msg.as_string())
  server.quit()


# limit: 每封邮件限制人数
def SendEmail(msg, limit=10):
  from_addr = config.GetConfig('email', 'from')
  to_addrs = config.GetConfig('email', 'to')
  password = config.GetConfig('email', 'password')
  smtp_server = config.GetConfig('email', 'smtp', 'server')
  smtp_port = config.GetConfig('email', 'smtp', 'port')
  if to_addrs is None or to_addrs == []:
    return
  msg['From'] = FormatAddr('ConanYu@foxmail.com')
  while len(to_addrs) > 0:
    cur_to_addrs = to_addrs[:limit]
    msg['To'] = FormatAddr(', '.join(cur_to_addrs))
    SendEmailFunc(from_addr, cur_to_addrs, password, smtp_server, smtp_port, msg)
    to_addrs = to_addrs[limit:]