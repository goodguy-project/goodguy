import asyncio

from goodguy.feishu.serve import serve as feishu_serve


def main():
    asyncio.run(feishu_serve())


if __name__ == '__main__':
    main()
