import json
import logging

from goodguy.feishu.send_message import send_message, send_card_message
from goodguy.order.order import order
from goodguy.timer.contest.data import insert_feishu_chat_id, delete_feishu_chat_id


def message_receive(body):
    try:
        if body["header"]["event_type"] != "im.message.receive_v1":
            return
        chat_id = body["event"]["message"]["chat_id"]
        # 仅支持text类content
        text: str = json.loads(body["event"]["message"]["content"])["text"]
        logging.debug(chat_id)
        # 去除at信息
        try:
            for mention in body["event"]["message"]["mentions"]:
                text = text.replace(mention["key"], "")
        except KeyError:
            pass
        result = order(text, 'feishu')
        if result["type"] == 'send':
            send_message({
                "receive_id": chat_id,
                "content": json.dumps(result["content"]),
                "msg_type": result["msg_type"],
            }, 'chat_id')
        elif result["type"] == 'card':
            send_card_message({
                "chat_id": chat_id,
                "msg_type": result["msg_type"],
                "card": result["content"],
            })
        elif result["type"] == 'remind':
            insert_feishu_chat_id(chat_id)
        elif result["type"] == 'forget':
            delete_feishu_chat_id(chat_id)
    except Exception as e:
        logging.exception(e)
