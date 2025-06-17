# -*- coding: utf-8 -*-
# @Time    : 2018/7/19 下午5:23
# @Author  : WangJuan
# @File    : Email.py

"""
封装发送邮件的方法

"""
import smtplib
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from loguru import logger


class SendMail:

    def __init__(self):
        self.log = logger

    def sendEmail(self, resp_time_list, result):
        msg = MIMEMultipart()

        body2 = 'Hi，all\n本次接口自动化测试报告如下：\n   接口响应时间集：%s\n   接口运行结果集：%s' % (resp_time_list, result)
        mail_body2 = MIMEText(body2, _subtype='plain', _charset='utf-8')
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        msg['Subject'] = Header("接口自动化测试报告"+"_"+tm, 'utf-8')
        msg['From'] = self.config.sender
        receivers = self.config.receiver
        toclause = receivers.split(',')
        msg['To'] = ",".join(toclause)
        msg.attach(mail_body2)

        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.config.smtpserver)
            smtp.login(self.config.username, self.config.password)
            smtp.sendmail(self.config.sender, toclause, msg.as_string())
        except Exception as e:
            print(e)
            print("发送失败")
            self.log.error("邮件发送失败，请检查邮件配置")

        else:
            print("发送成功")
            self.log.info("邮件发送成功")
        finally:
            smtp.quit()