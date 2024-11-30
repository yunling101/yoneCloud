#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.common import api
from django.core.serializers import serialize
from webserver.common.views import LoginValidate, BaseView
from webserver.SystemManage.models import Recycle, Config
from webserver.website.lang.zh_ch import Lang
from webserver.common.permissions import PermissionViewMixin
from webserver.ResourceManage.models import Hosts
from operator import itemgetter


class SystemConfig(BaseView):
    """
        站点配置
    """
    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        data = serialize('json', Config.objects.all())
        for line in api.Api.json_load(data):
            sline = line["fields"]
            sline["id"] = line["pk"]
            sline["config"] = api.Api.json_load(sline["config"])
            info["rows"].append(sline)

        info["code"] = True
        info["total"] = len(info["rows"])
        return info

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            config = Config.objects.filter(ename=data["id"])
            if len(config) == 1:
                tmp_config, authorize_cache = [], config[0].config
                for line in api.Api.json_load(config[0].config):
                    if line["ename"] != "logo" and line["ename"] != "version":
                        line["value"] = data[line["ename"]].replace("\r\n", "\n")
                    tmp_config.append(line)
                config.update(config=api.Api.json_dump(tmp_config))
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class SystemRecycleDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        资源回收站删除
    """
    permission_view = "delete_recycle"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            for ids in request_id.split(","):
                Recycle.objects.filter(id=int(ids)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class SystemRecycleDestroy(LoginValidate, PermissionViewMixin, BaseView):
    """
        资源回收站清空
    """
    permission_view = "destroy_recycle"

    def post(self, request):
        info = {"code": False, "msg": ""}
        try:
            if request.user.is_superuser:
                Recycle.objects.all().delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class SystemRecycleRestore(LoginValidate, PermissionViewMixin, BaseView):
    """
        还原资源
    """
    permission_view = "restore_recycle"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            if request_id == "all":
                recycle = Recycle.objects.all()
            else:
                recycle = Recycle.objects.none()
                for ids in request_id.split(","):
                    recycle |= Recycle.objects.filter(id=int(ids))

            for r in recycle:
                if r.type == "hosts":
                    data = api.Api.json_load(r.data)
                    handle_lists = ["certificate", "business", "role"]
                    certificate, business, role = itemgetter(*handle_lists)(data)
                    for k in handle_lists:
                        data.pop(k)

                    hosts = Hosts(**data)
                    hosts.certificate.set(certificate)
                    hosts.business.set(business)
                    hosts.role.set(role)
                    hosts.save()

            recycle.delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info
