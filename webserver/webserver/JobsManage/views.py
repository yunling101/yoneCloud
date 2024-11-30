#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.common import api
from webserver.common.views import LoginValidate, BaseView
from webserver.common.permissions import PermissionViewMixin
from django.core.serializers import serialize
from webserver.JobsManage.models import JobsNotify, JobsTemplate
from webserver.website.lang.zh_ch import Lang


class JobsTemplateList(LoginValidate, PermissionViewMixin, BaseView):
    """
        作业模板列表
    """
    permission_view = "view_jobs_template"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', JobsTemplate.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["content"] = str(e)
        return info


class JobsTemplateAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑作业模板
    """
    permission_view = "add_jobs_template"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            if data.get("id") == "":
                name = JobsTemplate.objects.filter(name=data["name"])
                if len(name) == 0:
                    template = JobsTemplate()
                    template.name = data.get("name")
                    template.content = data.get("content")
                    template.status = True if data.get("status") == "1" else False
                    template.comment = data.get("comment")
                    template.save()
                    info["code"] = True
                else:
                    info["msg"] = "模板名称已存在！"
            else:
                JobsTemplate.objects.filter(id=int(data["id"])).update(
                    name=data.get("name"),
                    content=data.get("content"),
                    status=True if data.get("status") == "1" else False,
                    comment=data.get("comment")
                )
                info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class JobsTemplateDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除作业模板
    """
    permission_view = "delete_jobs_template"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            JobsTemplate.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class JobsNotifyList(LoginValidate, PermissionViewMixin, BaseView):
    """
        作业通知列表
    """
    permission_view = "view_jobs_notify"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', JobsNotify.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["content"] = str(e)
        return info


class JobsNotifyAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑作业通知
    """
    permission_view = "add_jobs_notify"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            if data.get("id") == "":
                name = JobsNotify.objects.filter(name=data["name"])
                if len(name) == 0:
                    notify = JobsNotify()
                    notify.name = data.get("name")
                    notify.alias = data.get("alias")
                    notify.address = data.get("address")
                    notify.content = data.get("content")
                    notify.status = True if data.get("status") == "1" else False
                    notify.comment = data.get("comment")
                    notify.save()
                    info["code"] = True
                else:
                    info["msg"] = "模板名称已存在！"
            else:
                JobsNotify.objects.filter(id=int(data["id"])).update(
                    name=data.get("name"),
                    alias=data.get("alias"),
                    address=data.get("address"),
                    content=data.get("content"),
                    status=True if data.get("status") == "1" else False,
                    comment=data.get("comment")
                )
                info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class JobsNotifyDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除作业通知
    """
    permission_view = "delete_jobs_notify"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            JobsNotify.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info
