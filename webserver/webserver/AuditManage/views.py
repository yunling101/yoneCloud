#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.AuditManage.models import Login, Option, ConnectRecord, CommandRecord
from webserver.common import api
from django.core.serializers import serialize
from webserver.common.views import BaseView
from webserver.ResourceManage.models import Hosts
from webserver.UserManage.models import User


class AuditLogin(BaseView):
    """
        登录审计
    """
    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', Login.objects.all().order_by('-logout_added'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            api.logger.error("{0}".format(str(e)))
            info["content"] = str(e)
        return info


class AuditOption(BaseView):
    """
        操作审计
    """
    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', Option.objects.all().order_by('-date_added'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            api.logger.error("{0}".format(str(e)))
            info["content"] = str(e)
        return info


class AuditDetailCommand(BaseView):
    """
        命令历史
    """
    def get(self, request):
        info = {"code": False, "msg": "", "data": []}
        request_id = int(self.args[0])
        try:
            connect = ConnectRecord.objects.filter(id=request_id)
            if len(connect) == 1:
                command = CommandRecord.objects.filter(log_id=connect[0].id).order_by("-datetime")[:100]
                for line in command:
                    info["data"].append({
                        "datetime": "{0}".format(line.datetime),
                        "command": line.command
                    })
                info["code"] = True
            else:
                info["msg"] = "查找ID不存在！"
        except Exception as e:
            api.logger.error("{0}".format(str(e)))
            info["msg"] = str(e)
        return info


class AuditDetailPlayback(BaseView):
    """
        历史命令回放
    """
    def get(self, request):
        info = {"code": False, "msg": "", "data": ""}
        request_id = int(self.args[0])
        try:
            connect = ConnectRecord.objects.filter(id=request_id)
            if len(connect) == 1:
                v = connect[0].start_time
                h = Hosts.objects.filter(id=int(connect[0].server_id))
                u = User.objects.filter(id=int(connect[0].username_id))
                if len(h) == 1 and len(u) == 1:
                    log_date = "{0}-{1}-{2}".format(v.year, v.month, v.day)
                    info["data"] = {
                        "path": "/media/{0}/{1}".format(log_date, connect[0].log),
                        "username": u[0].username,
                        "hosts": h[0].ip,
                        "start_time": "{0}".format(connect[0].start_time.strftime("%Y年%m月%d日 %H:%M:%S"))
                    }
                    info["code"] = True
                else:
                    info["msg"] = "信息获取失败！"
            else:
                info["msg"] = "查找ID不存在！"
        except Exception as e:
            api.logger.error("{0}".format(str(e)))
            info["msg"] = str(e)
        return info
