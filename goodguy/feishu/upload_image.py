import json

import requests
from loguru import logger
from retrying import retry

from goodguy.feishu.access_token import get_tenant_access_token


# return image card
@retry(stop_max_attempt_number=5, wait_fixed=20000)
def upload_image(path: str, **kwargs) -> str:
    tenant_access_token = get_tenant_access_token()
    resp = requests.post('https://open.feishu.cn/open-apis/im/v1/images', headers={
        "Authorization": f"Bearer {tenant_access_token}",
    }, data={
        "image_type": kwargs.get("image_type", "message"),
    }, files={
        "image": open(path, 'rb'),
    })
    logger.debug(resp.text)
    obj = json.loads(resp.text)
    return obj["data"]["image_key"]
