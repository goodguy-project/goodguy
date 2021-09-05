import json
import logging
from typing import Dict
import requests
from retrying import retry
from goodguy.feishu.access_token import get_tenant_access_token


# doc: https://open.feishu.cn/document/ukTMukTMukTM/ucDO1EjL3gTNx4yN4UTM
@retry(stop_max_attempt_number=5, wait_fixed=20000)
def send_message(request: Dict, receive_id_type: str) -> None:
    tenant_access_token = get_tenant_access_token()
    rsp = requests.post(
        f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}",
        data=json.dumps(request),
        headers={
            "Authorization": f"Bearer {tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8",
        }
    )
    logging.debug(rsp.text)


# doc: https://open.feishu.cn/document/ukTMukTMukTM/uYTNwUjL2UDM14iN1ATN
@retry(stop_max_attempt_number=5, wait_fixed=20000)
def send_card_message(request: Dict) -> None:
    tenant_access_token = get_tenant_access_token()
    rsp = requests.post(
        "https://open.feishu.cn/open-apis/message/v4/send/",
        data=json.dumps(request),
        headers={
            "Authorization": f"Bearer {tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8",
        }
    )
    logging.debug(rsp.text)
