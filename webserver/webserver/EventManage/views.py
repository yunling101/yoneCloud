#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.EventManage.models import Event
from django.core.serializers import serialize
from webserver.common import api
from webserver.website.lang.zh_ch import Lang
from webserver.common.views import LoginValidate, BaseView
from webserver.common.permissions import PermissionViewMixin


class EventList(LoginValidate, PermissionViewMixin, BaseView):
    """
        事件管理列表
    """
    permission_view = "view_event"
    operation_record = False

    def get(self, request, *args, **kwargs):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', Event.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["content"] = str(e)
        return info


class EventDetail(BaseView):
    """
        事件详情
    """
    def get(self, *args, **kwargs):
        info = {"code": False, "msg": ""}
        request_id = int(self.args[0])
        data = serialize('json', Event.objects.filter(id=request_id))
        for line in api.Api.json_load(data):
            sd = line["fields"]
            sd["id"] = line["pk"]
            info["msg"] = sd
        info["code"] = True
        Event.objects.filter(id=request_id).update(status=False)
        return info


class EventDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除事件
    """
    permission_view = "delete_event"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            for ids in request_id.split(","):
                Event.objects.filter(id=int(ids)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class EventChange(BaseView):
    """
        事件状态
    """
    def post(self, request, *args, **kwargs):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        request_params = request.POST.get("params", None)
        try:
            if request_params == "all":
                Event.objects.filter(status=True).update(status=False)
            else:
                for ids in request_id.split(","):
                    Event.objects.filter(id=int(ids)).update(status=False)
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info
