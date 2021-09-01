import os
import sys

import requests


def build():
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)
    pb_path = os.path.join(root, 'goodguy', 'pb')
    if not os.path.exists(pb_path):
        os.mkdir(pb_path)
    crawl_service_proto_path = os.path.join(pb_path, 'crawl_service.proto')
    with open(crawl_service_proto_path, 'w', encoding='utf-8') as pb_file:
        pb_file.write(requests.get(
            # 使用镜像
            "https://mirror.ghproxy.com/"
            "https://raw.githubusercontent.com/goodguy-project/goodguy-crawl/main/crawl_service/crawl_service.proto",
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/91.0.4472.164 Safari/537.36",
            }).text)
    os.system(f'{sys.executable} -m grpc_tools.protoc -I{root} --python_out={root} --grpc_python_out={root} '
              f'{crawl_service_proto_path}')


if __name__ == '__main__':
    build()
