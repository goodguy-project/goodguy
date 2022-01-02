import smtplib
from email.mime.text import MIMEText
from typing import List

from goodguy.service.email_subscription import get_subscriber
from goodguy.util.config import GLOBAL_CONFIG


def split_to_addr(to_addr: List[str], max_send: int = 10) -> List[List[str]]:
    ret: List[List[str]] = []
    for to in to_addr:
        if not ret or len(ret[-1]) >= max_send:
            ret.append([])
        ret[-1].append(to)
    return ret


def send_email(from_addr: str, to_addrs: List[str], password: str, smtp_server: str, smtp_port: int, mail: MIMEText):
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addrs, mail.as_string())
    server.quit()


def send_all_email(t: str, title: str, text: str, max_send: int = 20) -> None:
    from_addr = GLOBAL_CONFIG.get("email.from")
    to_addr = get_subscriber()
    password = GLOBAL_CONFIG.get("email.password")
    smtp_server = GLOBAL_CONFIG.get("email.smtp.server")
    smtp_port = GLOBAL_CONFIG.get("email.smtp.port")
    if not to_addr:
        return
    for to in split_to_addr(to_addr, max_send):
        mail = MIMEText(text, t, 'utf-8')
        mail['Subject'] = title
        mail['From'] = from_addr
        mail['To'] = ', '.join(to)
        send_email(from_addr, to, password, smtp_server, smtp_port, mail)
