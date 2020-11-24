import smtplib
import goodguy.util.config as config
from email.header import Header
from email.utils import parseaddr, formataddr


def format_addr(s):
  name, addr = parseaddr(s)
  return formataddr((Header(name, 'utf-8').encode(), addr))


def SendEmailFunc(from_addr, to_addrs: list, password, smtp_server, smtp_port, msg):
  server = smtplib.SMTP_SSL(smtp_server, smtp_port)
  server.login(from_addr, password)
  server.sendmail(from_addr, to_addrs, msg.as_string())
  server.quit()


def SendEmail(msg):
  from_addr = config.GetConfig('email', 'from')
  to_addrs = config.GetConfig('email', 'to')
  password = config.GetConfig('email', 'password')
  smtp_server = config.GetConfig('email', 'smtp', 'server')
  smtp_port = config.GetConfig('email', 'smtp', 'port')
  if to_addrs is None or to_addrs == []:
    return
  msg['From'] = format_addr('ConanYu <ConanYu@foxmail.com>')
  for to_addr in to_addrs:
    msg['To'] = format_addr(f'{to_addr} <{to_addr}>')
    SendEmailFunc(from_addr, [to_addr], password, smtp_server, smtp_port, msg)