import os
from typing import Set

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_Base = declarative_base()


class FeishuNotice(_Base):
    __tablename__ = 'feishu_notice'
    index = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(20))


class EmailNotice(_Base):
    __tablename__ = 'email_notice'
    index = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50))


# 创建数据库
_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.sqlite3')
_engine = create_engine(f'sqlite:///{_DB_PATH}')
_Base.metadata.create_all(_engine)
# 提供给用户的类
Session = sessionmaker(bind=_engine)


def insert_feishu_chat_id(chat_id: str):
    session = Session()
    feishu = FeishuNotice(chat_id=chat_id)
    session.add(feishu)
    session.commit()


def select_all_feishu_chat_id() -> Set[str]:
    session = Session()
    return set(e.chat_id for e in session.query(FeishuNotice).all())


def delete_feishu_chat_id(chat_id: str):
    session = Session()
    session.query(FeishuNotice).filter(FeishuNotice.chat_id == chat_id).delete(synchronize_session=False)
    session.commit()


if __name__ == '__main__':
    insert_feishu_chat_id("11")
    print(select_all_feishu_chat_id())
    delete_feishu_chat_id("11")
    print(select_all_feishu_chat_id())
