import os
from promise import Promise

notice_id = set()
tmp_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notice.tmp')


# 从文件中读取数据
def LoadFromNoticeId():
    global tmp_file_path, notice_id
    if not os.path.exists(tmp_file_path):
        return
    with open(tmp_file_path, 'r', encoding='utf-8') as f:
        notice_ids = f.read().split(',')
        for a_notice_id in notice_ids:
            notice_id.add(a_notice_id)


# 一启动就读文件
LoadFromNoticeId()


# 异步更新到文件中 有极小概率有更新失败的情况
def UpdateNoticeId():
    global tmp_file_path, notice_id
    def UpdateNoticeIdInner():
        with open(tmp_file_path, 'w', encoding='utf-8') as f:
            s = ''
            for a_notice_id in notice_id:
                if s != '':
                    s += ','
                s += a_notice_id
            f.write(s)
    Promise(UpdateNoticeIdInner).start()


def AddNoticeId(message_type, send_id):
    notice_id.add(message_type + "|" + send_id)
    UpdateNoticeId()


def RemoveNoticeId(message_type, send_id):
    notice_id.remove(message_type + "|" + send_id)
    UpdateNoticeId()