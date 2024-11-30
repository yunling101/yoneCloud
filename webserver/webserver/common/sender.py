#!/usr/bin/env python
# -*- coding:utf-8 -*-

import smtplib

from . import api
from email.mime.text import MIMEText
from webserver.SystemManage.models import Config


class SenderMail(object):
    """
        邮件发送
    """
    @classmethod
    def login(cls):
        info = {"code": False, "msg": ""}
        try:
            cfg = Config.objects.filter(ename="email")
            if len(cfg) == 1:
                obj = {}
                for c in api.Api.json_load(cfg[0].config):
                    if c.get("value"):
                        obj[c.get("ename")] = c.get("value")
                    else:
                        api.logger.error("{0}".format("{0}配置不能为空！".format(c.get("cname"))))
                        info["msg"] = "邮箱服务配置错误, 无法发送验证码, 请联系管理员！"
                        return info
                info["code"] = True
                info["msg"] = obj
            else:
                info["msg"] = "邮箱配置不存在！"
        except Exception as e:
            api.logger.error("{0}".format(str(e)))
            info["msg"] = "未知异常错误！"
        return info

    @classmethod
    def sender(cls, email, msg, title):
        info = {"code": False, "msg": ""}
        try:
            login_info = cls.login()
            if login_info.get("code"):
                login = login_info.get("msg")
                text = MIMEText(msg, "html", "utf-8")
                text["Subject"] = title
                text["From"] = login.get("username")
                text["To"] = email

                server = smtplib.SMTP(login.get("server"), int(login.get("port")), None, 10)
                server.set_debuglevel(0)
                server.login(login.get("username"), login.get("password"))
                server.sendmail(login.get("username"), email, text.as_string())
                server.close()
                info["code"] = True
            else:
                info["msg"] = login_info.get("msg")
        except Exception as e:
            api.logger.error("{0}".format(str(e)))
            info["msg"] = "未知异常错误！"
        return info
