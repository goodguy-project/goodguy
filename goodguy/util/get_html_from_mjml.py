import os
import time
import random

from goodguy.util.const import ROOT


def get_html_from_mjml(mjml: str) -> str:
    path = os.path.join(ROOT, '.tmp')
    if not os.path.exists(path):
        os.mkdir(path)

    name = f'{int(time.time())}_{random.randint(0, 998244353)}'
    file_mjml = os.path.join(path, f'{name}.mjml')
    file_html = os.path.join(path, f'{name}.html')
    with open(file_mjml, 'w', encoding='utf-8') as f:
        f.write(mjml)
    code = os.system(f'mjml {file_mjml} -o {file_html}')
    if code != 0:
        raise RuntimeError('run mjml fail')
    with open(file_html, 'r', encoding='utf-8') as f:
        return f.read()
