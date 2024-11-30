#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.common import api
from webserver.common.views import LoginValidate, BaseView
from django.core.serializers import serialize
from webserver.website.lang.zh_ch import Lang
from uuid import uuid1
from webserver.TaskManage.models import TaskTimer, TaskTimerResults
from webserver.common.permissions import PermissionViewMixin
from webserver.ResourceManage.models import Hosts
from django.db.models import Q
from webserver.common.regular import RegEx


class TaskTimerLists(LoginValidate, PermissionViewMixin, BaseView):
    """
        定时任务列表
    """
    permission_view = "view_task_timer"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', TaskTimer.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["content"] = str(e)
        return info


class TaskTimerAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑定时任务
    """
    permission_view = "add_task_timer"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        username = request.user.username
        try:
            data = api.Api.json_load(request_data)
            if data.get("execution_time") is not None and data.get("execution_time") != "":
                # if RegEx.cron(data.get("execution_time")) is None:
                expr = data.get("execution_time").split(" ")
                if len(expr) != 5 or "" in expr:
                    info["msg"] = "执行时间格式错误！"
                    return info
            else:
                info["msg"] = "执行时间不能为空！"
                return info

            task_hosts = []
            if data.get("hosts") is not None:
                for h in data.get("hosts").split(","):
                    hosts = Hosts.objects.filter(hostname=h)
                    task_hosts.extend(hosts)
            if data.get("business") is not None:
                for b in data.get("business").split(","):
                    if b == "默认业务":
                        hosts = Hosts.objects.filter(Q(business__name=b) | Q(business=None))
                    else:
                        hosts = Hosts.objects.filter(business__name=b)
                    task_hosts.extend(hosts)

            if data.get("id") == "":
                save_uuid = str(uuid1())
                timer = TaskTimer.objects.filter(name=data["name"])
                if len(timer) == 0:
                    t = TaskTimer()
                    t.name = data.get("name")
                    t.uuid = save_uuid
                    t.username = username
                    t.timer_type = data.get("timer_type")
                    t.retry_count = data.get("retry_count")
                    t.execution_time = data.get("execution_time")
                    t.scripts = data.get("scripts").replace("\r\n", "\\n")
                    t.description = data.get("description")
                    t.status = True
                    t.save()

                    for h in task_hosts:
                        t.hosts.add(h)
                    t.save()

                    info["code"] = True
                else:
                    info["msg"] = "任务名称已存在！"
            else:
                timer = TaskTimer.objects.filter(id=int(data.get("id")))
                if len(timer) == 1:
                    timer.update(
                        name=data.get("name"),
                        timer_type=data.get("timer_type"),
                        retry_count=data.get("retry_count"),
                        execution_time=data.get("execution_time"),
                        scripts=data.get("scripts"),
                        description=data.get("description")
                    )
                    timer[0].hosts.clear()

                    for h in task_hosts:
                        timer[0].hosts.add(h)
                    timer[0].save()

                    info["code"] = True
                else:
                    info["msg"] = "任务查找出错！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class TaskTimerDetail(BaseView):
    """
        执行结果查看
    """

    def get(self, *args, **kwargs):
        info = {"code": False, "msg": ""}
        request_id = int(self.args[0])
        timer = TaskTimer.objects.filter(id=request_id)
        if len(timer) == 1:
            data = serialize('json', TaskTimerResults.objects.filter(uuid=timer[0].uuid).order_by('-start_time'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["msg"] = sd
                break
        info["code"] = True
        return info


class TaskTimerDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除定时任务
    """
    permission_view = "delete_task_timer"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            TaskTimer.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info
