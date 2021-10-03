import logging
from typing import Dict, Optional

from goodguy.order.recent_contest_parser import recent_contest_parser, recent_contest_card_parser
from goodguy.util.const import USAGE
from goodguy.order.user_contest_record_parser import user_contest_record_parser, user_contest_record_card_parser
from goodguy.service.crawl import get_recent_contest, get_user_contest_record
from goodguy.util.config import GLOBAL_CONFIG
from goodguy.util.const import PLATFORM_ALL


# pylint: disable=too-many-return-statements
def order(text: str, sns: Optional[str] = None) -> Dict:
    text_split = text.split()
    op = '' if len(text_split) <= 0 else text_split[0]
    op = {
        "cf": "codeforces",
        "atc": "atcoder",
        "nc": "nowcoder",
        "lc": "leetcode",
        "lg": "luogu",
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
    if op == 'reload_config':
        GLOBAL_CONFIG.reload_config()
        logging.info('reload config succeed')
        return {
            "type": 'send',
            "content": {
                "text": 'reload config succeed',
            },
            "msg_type": "text",
        }
    if op == 'remind':
        return {
            "type": 'remind',
        }
    if op == 'forget':
        return {
            "type": 'forget',
        }
    if op in PLATFORM_ALL:
        if handle != '' and op in {'codeforces', 'atcoder', 'nowcoder', 'leetcode'}:
            data = get_user_contest_record(op, handle)
            if sns == 'feishu':
                return {
                    "type": 'card',
                    "content": user_contest_record_card_parser(handle, op, data),
                    "msg_type": "interactive",
                }
            return {
                "type": 'send',
                "content": {
                    "text": user_contest_record_parser(handle, op, data),
                },
                "msg_type": "text",
            }
        if handle == '' and op in {'codeforces', 'nowcoder', 'atcoder', 'leetcode', 'luogu'}:
            data = get_recent_contest(op)
            if sns == 'feishu':
                return {
                    "type": 'card',
                    "content": recent_contest_card_parser(op, data),
                    "msg_type": "interactive",
                }
            return {
                "type": 'send',
                "content": {
                    "text": recent_contest_parser(op, data),
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
