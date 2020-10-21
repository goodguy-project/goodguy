import json, requests, config, common, time
from codeforces import GetCodeforcesPromise, CodeforcesDataToString
from atcoder import GetAtcoderPromise, AtcoderDataToString
from codeforces_contest import GetCodeforcesUpcomingContestPromise, CodeforcesUpcomingContestDataToString
from promise import Promise


def SendMessage(token, message_type, send_id, text=''):
    url = "https://open.feishu.cn/open-apis/message/v4/send/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
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


def HandleMessageThread(token, message_type, send_id, text=''):
    global kMenu
    try:
        if text is None:
            text = ''
        text_split = text.split()
        f = '' if len(text_split) <= 0 else text_split[0]
        handle = '' if len(text_split) <= 1 else text_split[1]
        if f in {'菜单', 'menu', ''}:
            SendMessage(token, message_type, send_id, text=kMenu)
        elif f == 'reload_config':
            config.ReloadConfig()
            print('reload config successd.')
        elif f in {'cf', 'CF', 'codeforces'}:
            if handle == '':
                start_time = common.GetTime()
                promise = GetCodeforcesUpcomingContestPromise()
                while not IsTimeOut(start_time) and not hasattr(promise, 'result'):
                    time.sleep(float(config.GetConfig('crawler', 'sleeptime', default=0.01)))
                if hasattr(promise, 'result'):
                    SendMessage(token, message_type, send_id,
                                text=CodeforcesUpcomingContestDataToString(promise.result))
                else:
                    SendMessage(token, message_type, send_id, text=f'命令 {text} 超时')
            else:
                start_time = common.GetTime()
                promise = GetCodeforcesPromise(handle.lower())
                while not IsTimeOut(start_time) and not hasattr(promise, 'result'):
                    time.sleep(float(config.GetConfig('crawler', 'sleeptime', default=0.01)))
                if hasattr(promise, 'result'):
                    SendMessage(token, message_type, send_id, text=CodeforcesDataToString(handle, promise.result))
                else:
                    SendMessage(token, message_type, send_id, text=f'命令 {text} 超时或无法找到该用户')
        elif f in {'atc', 'ATC', 'atcoder'}:
            start_time = common.GetTime()
            promise = GetAtcoderPromise(handle.lower())
            while not IsTimeOut(start_time) and not hasattr(promise, 'result'):
                time.sleep(float(config.GetConfig('crawler', 'sleeptime', default=0.01)))
            if hasattr(promise, 'result'):
                SendMessage(token, message_type, send_id, text=AtcoderDataToString(handle, promise.result))
            else:
                SendMessage(token, message_type, send_id, text=f'命令 {text} 超时或无法找到该用户')
        else:
            SendMessage(token, message_type, send_id, text=f'未知命令 {text}，用法：\n{kMenu}')
            print(f'unknown command {f}.')
    except Exception as e:
        print(e)


def HandleMessage(token, message_type, send_id, text=''):
    Promise(HandleMessageThread, (token, message_type, send_id, text)).start()


if __name__ == "__main__":
    promise = GetCodeforcesPromise('ConanYu')
    while not hasattr(promise, 'result'):
        time.sleep(float(config.GetConfig('crawler', 'sleeptime', default=0.01)))
    print(promise.result)
    promise = GetCodeforcesPromise('ConanYu')
    while not hasattr(promise, 'result'):
        time.sleep(float(config.GetConfig('crawler', 'sleeptime', default=0.01)))
    print(promise.result)
