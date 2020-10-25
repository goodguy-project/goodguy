import json, requests, config, common, time
from codeforces import GetCodeforcesPromise, CodeforcesDataToString
from atcoder import GetAtcoderPromise, AtcoderDataToString
from codeforces_contest import GetCodeforcesUpcomingContestPromise, CodeforcesUpcomingContestDataToString
from promise import Promise
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


kMenu = '''1.查询用户Codeforces情况，样式：`cf 用户名`
2.查询用户Atcoder情况，样式：`atc 用户名`
3.查询Codeforces最近比赛，样式：`cf`'''


def IsTimeOut(start_time):
    now = common.GetTime()
    return now - start_time > float(config.GetConfig('crawler', 'timeout', default=15)) * (10 ** 9)


def HandleMessageThread(message_type, send_id, text=''):
    global kMenu
    try:
        if text is None:
            text = ''
        text_split = text.split()
        f = '' if len(text_split) <= 0 else text_split[0]
        handle = '' if len(text_split) <= 1 else text_split[1]
        f = f.lower()
        # 查询菜单
        if f in {'菜单', 'menu', ''}:
            SendMessage(message_type, send_id, text=kMenu)
        elif f == 'reload_config':
            config.ReloadConfig()
            print('reload config successd.')
        # 查询Codeforces信息
        elif f in {'cf', 'codeforces'}:
            # 查询Codeforces最近比赛
            if handle == '':
                start_time = common.GetTime()
                promise = GetCodeforcesUpcomingContestPromise()
                while not IsTimeOut(start_time) and not hasattr(promise, 'result'):
                    time.sleep(float(config.GetConfig('crawler', 'sleeptime', default=0.01)))
                if hasattr(promise, 'result'):
                    SendMessage(message_type, send_id,
                                text=CodeforcesUpcomingContestDataToString(promise.result))
                else:
                    SendMessage(message_type, send_id, text=f'命令 {text} 超时')
            # 查询Codeforces用户
            else:
                start_time = common.GetTime()
                promise = GetCodeforcesPromise(handle.lower())
                while not IsTimeOut(start_time) and not hasattr(promise, 'result'):
                    time.sleep(float(config.GetConfig('crawler', 'sleeptime', default=0.01)))
                if hasattr(promise, 'result'):
                    SendMessage(message_type, send_id, text=CodeforcesDataToString(handle, promise.result))
                else:
                    SendMessage(message_type, send_id, text=f'命令 {text} 超时或无法找到该用户')
        # 查询Atcoder信息
        elif f in {'atc', 'atcoder'}:
            start_time = common.GetTime()
            promise = GetAtcoderPromise(handle.lower())
            while not IsTimeOut(start_time) and not hasattr(promise, 'result'):
                time.sleep(float(config.GetConfig('crawler', 'sleeptime', default=0.01)))
            if hasattr(promise, 'result'):
                SendMessage(message_type, send_id, text=AtcoderDataToString(handle, promise.result))
            else:
                SendMessage(message_type, send_id, text=f'命令 {text} 超时或无法找到该用户')
        # 未知输入
        else:
            SendMessage(message_type, send_id, text=f'未知命令 {text}，用法：\n{kMenu}')
    except Exception as e:
        print(e)


def HandleMessage(message_type, send_id, text=''):
    Promise(HandleMessageThread, (message_type, send_id, text)).start()


if __name__ == "__main__":
    promise = GetCodeforcesPromise('ConanYu')
    while not hasattr(promise, 'result'):
        time.sleep(float(config.GetConfig('crawler', 'sleeptime', default=0.01)))
    print(promise.result)
    promise = GetCodeforcesPromise('ConanYu')
    while not hasattr(promise, 'result'):
        time.sleep(float(config.GetConfig('crawler', 'sleeptime', default=0.01)))
    print(promise.result)
