import json, requests
import goodguy.feishu.message as message
import goodguy.util.config as config
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    # 解析请求 body
    req_body = self.rfile.read(int(self.headers['content-length']))
    obj = json.loads(req_body.decode("utf-8"))
    print(req_body)
    # 校验 verification token 是否匹配，token 不匹配说明该回调并非来自开发平台
    token = obj.get("token", "")
    if token != config.GetConfig("app", "verification", "token"):
      print("verification token not match, token =", token)
      self.Response("")
      return
    # 根据 type 处理不同类型事件
    type = obj.get("type", "")
    if "url_verification" == type:  # 验证请求 URL 是否有效
      self.HandleRequestUrlVerify(obj)
    elif "event_callback" == type:  # 事件回调
      # 获取事件内容和类型，并进行相应处理，此处只关注给机器人推送的消息事件
      event = obj.get("event")
      if event.get("type", "") == "message":
        self.HandleMessage(event)
        return

  def HandleRequestUrlVerify(self, post_obj):
    # 原样返回 challenge 字段内容
    challenge = post_obj.get("challenge", "")
    rsp = {'challenge': challenge}
    self.Response(json.dumps(rsp))

  def HandleMessage(self, event):
    # 此处只处理 text 类型消息，其他类型消息忽略
    msg_type = event.get("msg_type", "")
    if msg_type != "text":
      print("unknown msg_type =", msg_type)
      return
    # 调用发消息 API 之前，先要获取 API 调用凭证：tenant_access_token
    if event.get('open_chat_id', None) is not None:
      message.HandleMessage('chat_id', event.get('open_chat_id'), event.get("text_without_at_bot"))
    elif event.get('open_id', None) is not None:
      message.HandleMessage('open_id', event.get('open_id'), event.get('text_without_at_bot'))
    else:
      print('unknown message')

  def Response(self, body):
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    self.wfile.write(body.encode())


def run():
  port = config.GetConfig("http", "port")
  server_address = ('', port)
  httpd = HTTPServer(server_address, RequestHandler)
  print("GoodGuy is running...")
  httpd.serve_forever()


if __name__ == '__main__':
  run()
