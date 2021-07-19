import json
import logging
from typing import Dict
import requests
from retrying import retry
from goodguy.feishu.access_token import get_tenant_access_token


# request结构： https://open.feishu.cn/document/ukTMukTMukTM/ucDO1EjL3gTNx4yN4UTM
@retry(stop_max_attempt_number=5, wait_fixed=20)
def send_message(request: Dict, receive_id_type: str):
    tenant_access_token = get_tenant_access_token()
    rsp = requests.post(
        f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}",
        data=json.dumps(request),
        headers={
            "Authorization": f"Bearer {tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8",
        }
    )
    logging.debug(rsp)
