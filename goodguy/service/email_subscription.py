import hashlib
import json
import logging
import traceback
from typing import Union, List

import requests

from goodguy.util.config import GLOBAL_CONFIG


def md5(v: Union[str, int]) -> str:
    if isinstance(v, int):
        v = str(v)
    o = hashlib.md5()
    o.update(v.encode('utf-8'))
    return o.hexdigest()


def get_subscriber() -> List[str]:
    try:
        host = GLOBAL_CONFIG.get('email_subscription.host', 'localhost')
        port = GLOBAL_CONFIG.get('email_subscription.port', 9853)
        email = GLOBAL_CONFIG.get('email_subscription.admin.email')
        pwd = md5(GLOBAL_CONFIG.get('email_subscription.admin.password'))
        session = requests.Session()
        session.post(f'{host}:{port}/api/login', headers={
            'Content-Type': 'application/json',
        }, data=json.dumps({
            'email': email,
            'password': pwd,
        }))
        response = session.get(f'{host}:{port}/api/subscriber')
        return json.loads(response.text)
    except Exception as e:
        traceback.print_stack()
        logging.error(e)
    return []


if __name__ == '__main__':
    print(get_subscriber())
