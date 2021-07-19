import json
import logging

from goodguy.feishu.send_message import send_message
from goodguy.order.order import order


def message_receive(body):
    try:
        if body["header"]["event_type"] != "im.message.receive_v1":
            return
        chat_id = body["event"]["message"]["chat_id"]
        # 仅支持text类content
        text: str = json.loads(body["event"]["message"]["content"])["text"]
        # 去除at信息
        try:
            for mention in body["event"]["message"]["mentions"]:
                text = text.replace(mention["key"], "")
        except KeyError:
            pass
        result = order(text)
        if result['type'] == 'send':
            send_message({
                "receive_id": chat_id,
                "content": json.dumps({
                    "text": result["text"],
                }),
                "msg_type": "text",
            }, 'chat_id')
    except Exception as e:
        logging.exception(e)
