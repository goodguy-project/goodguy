import logging
from typing import Dict

from goodguy.order.recent_contest_parser import recent_contest_parser
from goodguy.order.usage import USAGE
from goodguy.order.user_contest_record_parser import user_contest_record_parser
from goodguy.service.crawl import get_recent_contest, get_user_contest_record
from goodguy.util.config import GLOBAL_CONFIG


def order(text: str) -> Dict:
    text_split = text.split()
    op = '' if len(text_split) <= 0 else text_split[0]
    op = {
        "cf": "codeforces",
        "atc": "atcoder",
        "nc": "nowcoder",
        "lc": "leetcode",
    }.get(op, op)
    handle = '' if len(text_split) <= 1 else text_split[1]
    logging.debug(f"text: {text}\nop: {op}\nhandle: {handle}")
    op = op.lower()
    # 查询菜单
    if op in {'菜单', 'menu', ''}:
        return {
            "type": 'send',
            "content": {
                "text": USAGE,
            },
            "msg_type": "text",
        }
    # 重载配置文件（一般不使用）
    elif op == 'reload_config':
        GLOBAL_CONFIG.reload_config()
        logging.info('reload config succeed')
        return {
            "type": 'send',
            "content": {
                "text": 'reload config succeed',
            },
            "msg_type": "text",
        }
    elif op in {'codeforces', 'atcoder', 'nowcoder', 'leetcode'}:
        if handle != '' and op in {'codeforces', 'atcoder', 'nowcoder'}:
            return {
                "type": 'send',
                "content": {
                    "text": user_contest_record_parser(handle, op, get_user_contest_record(op)),
                },
                "msg_type": "text",
            }
        elif handle == '' and op in {'codeforces', 'atcoder', 'nowcoder', 'leetcode'}:
            return {
                "type": 'send',
                "content": {
                    "text": recent_contest_parser(op, get_recent_contest(op)),
                },
                "msg_type": "text",
            }
    # 未知输入
    return {
        "type": "send",
        "content": {
            "text": f'命令 {text} 发生未知错误，用法：\n{USAGE}',
        },
        "msg_type": "text",
    }
