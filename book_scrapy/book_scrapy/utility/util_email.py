# coding: utf-8
import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from utility import SMTP_SERVER


class EmailClient(object):
    # 初始化基本信息
    def __init__(self, host=SMTP_SERVER['HOST'], user=SMTP_SERVER['USER'], passwd=SMTP_SERVER['PASSWORD']):
        self._user = user
        self._me = user
        server = smtplib.SMTP()
        server.connect(host)
        server.login(self._user, passwd)
        self._server = server

    # 发送文件或html邮件
    def send(self, to_list, sub, content, subtype='html'):
        # 如果发送的是文本邮件，则_subtype设置为plain
        # 如果发送的是html邮件，则_subtype设置为html
        msg = MIMEText(content, _subtype=subtype, _charset='utf-8')
        sub = Header(sub, 'utf-8')
        msg['Subject'] = sub
        msg['From'] = self._me
        msg['To'] = ",".join(to_list)
        try:
            self._server.sendmail(self._me, to_list, msg.as_string())
            return True
        except Exception, e:
            logging.error(str(e))
            return False

    # 释放资源
    def __del__(self):
        # http://stackoverflow.com/questions/6270782/how-to-send-an-email-with-python
        if hasattr(self, '_server'):
            self._server.quit()
            self._server.close()