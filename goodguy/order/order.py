import logging
from typing import Dict
from goodguy.order.usage import USAGE
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
            "text": USAGE,
        }
    # 重载配置文件（一般不使用）
    elif op == 'reload_config':
        GLOBAL_CONFIG.reload_config()
        logging.info('reload config succeed')
        return {
            "type": 'send',
            "text": 'reload config succeed',
        }
    elif op in {'codeforces', 'atcoder', 'nowcoder', 'leetcode'}:
        if handle != '' and op in {'codeforces', 'atcoder', 'nowcoder'}:
            return {
                "type": 'send',
                "text": str(get_user_contest_record(op, handle))
            }
        elif handle == '' and op in {'codeforces', 'atcoder', 'nowcoder', 'leetcode'}:
            return {
                "type": 'send',
                "text": str(get_recent_contest(op)),
            }
    # 未知输入
    return {
        "type": "send",
        "text": f'命令 {text} 发生未知错误，用法：\n{USAGE}',
    }
