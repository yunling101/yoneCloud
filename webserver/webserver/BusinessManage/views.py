#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.core.serializers import serialize
from webserver.common.views import LoginValidate, BaseView
from webserver.BusinessManage.models import Business
from webserver.common import api
from webserver.website.lang.zh_ch import Lang
from webserver.common.permissions import PermissionViewMixin


class BusinessItem(LoginValidate, PermissionViewMixin, BaseView):
    """
        业务列表
    """
    permission_view = "view_business"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', Business.objects.all().order_by("id"))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["content"] = str(e)
        return info


class BusinessAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑业务
    """
    permission_view = "add_business"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            if data.get("id") == "":
                business = Business.objects.filter(name=data["name"])
                if len(business) == 0:
                    b = Business()
                    b.name = data.get("name")
                    b.life_cycle = data.get("life_cycle")
                    b.maintainer = data.get("maintainer")
                    b.tester = data.get("tester")
                    b.save()
                    info["code"] = True
                else:
                    info["msg"] = "业务名称已存在！"
            else:
                Business.objects.filter(id=int(data.get("id"))).update(
                    name=data.get("name"),
                    life_cycle=data.get("life_cycle"),
                    maintainer=data.get("maintainer"),
                    tester=data.get("tester")
                )
                info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class BusinessDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除业务
    """
    permission_view = "delete_business"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            Business.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info
