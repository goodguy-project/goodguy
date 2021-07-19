import logging
from typing import Dict
from goodguy.order.usage import USAGE
from goodguy.util.config import GLOBAL_CONFIG


def order(text: str) -> Dict:
    text_split = text.split()
    op = '' if len(text_split) <= 0 else text_split[0]
    handle = '' if len(text_split) <= 1 else text_split[1]
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
    # TODO 开发中
    # 未知输入
    return {
        "type": "send",
        "texts": f'命令 {text} 发生未知错误，用法：\n{USAGE}',
    }
