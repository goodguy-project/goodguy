import config, smtplib
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
  smtp_server = config.GetConfig('email', 'smtp', 'server')
  smtp_port = config.GetConfig('email', 'smtp', 'port')
  if to_addrs is None or to_addrs == []:
    return
  SendEmailFunc(from_addr, to_addrs, smtp_port, smtp_server, smtp_port, msg)