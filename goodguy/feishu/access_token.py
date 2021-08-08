import json
import logging

import requests
from cachetools.func import ttl_cache
from goodguy.util.config import GLOBAL_CONFIG
from retrying import retry


@retry(stop_max_attempt_number=5, wait_fixed=20000)
@ttl_cache(ttl=1200)
def get_tenant_access_token():
    app_id = GLOBAL_CONFIG.get("app.id")
    app_secret = GLOBAL_CONFIG.get("app.secret")
    text = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/",
        data=json.dumps({
            "app_id": app_id,
            "app_secret": app_secret,
        }), headers={
            "Content-Type": "application/json; charset=utf-8",
        }
    ).text
    logging.debug(text)
    return json.loads(text)["tenant_access_token"]


if __name__ == '__main__':
    logging.getLogger().setLevel(10)
    print(get_tenant_access_token())
