import json
import logging
import http
from http.server import BaseHTTPRequestHandler, HTTPServer
from concurrent.futures import ThreadPoolExecutor

from goodguy.feishu.message_receive import message_receive
from goodguy.util.config import GLOBAL_CONFIG

MESSAGE_RECEIVE_EXECUTOR = ThreadPoolExecutor(max_workers=20)


class FeishuRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):  # pylint: disable=invalid-name
        global MESSAGE_RECEIVE_EXECUTOR
        # 解析请求 body
        try:
            body = json.loads(self.rfile.read(int(self.headers['content-length'])).decode("utf-8"))
            # 校验 verification token 是否匹配，token 不匹配说明该回调并非来自开发平台
            try:
                token = body["header"]["token"]
            except KeyError:
                token = body["token"]
            if token != GLOBAL_CONFIG.get("feishu.app.token"):
                self.__response("", http.HTTPStatus.BAD_REQUEST)
                return
            # 验证请求 URL是否有效
            if body.get("type", "") == "url_verification":
                self.__response(json.dumps({
                    "challenge": body["challenge"]
                }))
                return
            self.__response("")
            MESSAGE_RECEIVE_EXECUTOR.submit(message_receive, body)
        except Exception as e:
            logging.exception(e)
            self.__response("", http.HTTPStatus.BAD_REQUEST)

    def __response(self, body: str, http_status=http.HTTPStatus.OK):
        self.send_response(http_status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(body.encode())


async def serve():
    host = GLOBAL_CONFIG.get("feishu.http.host", '')
    port = GLOBAL_CONFIG.get("feishu.http.port", 13331)
    address = host, port
    server = HTTPServer(address, FeishuRequestHandler)
    print("goodguy.feishu is running...")
    server.serve_forever()
