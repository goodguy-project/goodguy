import config, requests, json
from cache import AutoCache


def GetTenantAccessToken():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers = {
        "Content-Type": "application/json"
    }
    req_body = {
        "app_id": config.GetConfig("app", "id"),
        "app_secret": config.GetConfig("app", "secret")
    }
    data = bytes(json.dumps(req_body), encoding='utf8')
    try:
        req = requests.post(url=url, data=data, headers=headers)
        req = json.loads(req.text)
        return req.get('tenant_access_token', '')
    except Exception as e:
        print(e)
        return ''


# token过期时间设置为28分钟
token_cache = AutoCache(GetTenantAccessToken, 1680)


def SendMessage(message_type, send_id, text=''):
    url = "https://open.feishu.cn/open-apis/message/v4/send/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token_cache.Get()
    }
    req_body = {
        message_type: send_id,
        "msg_type": "text",
        "content": {
            "text": text
        }
    }
    try:
        data = bytes(json.dumps(req_body), encoding='utf-8')
        req = requests.post(url=url, data=data, headers=headers)
        print(req.text)
    except Exception as e:
        print(e)