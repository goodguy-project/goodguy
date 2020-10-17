import json, requests

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

def HandleMessage(token, message_type, send_id, text=''):
  pass