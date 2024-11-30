#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.common import api
from webserver.common.views import LoginValidate, BaseView
from django.core.serializers import serialize
from webserver.website.lang.zh_ch import Lang
from webserver.ResourceManage.models import Hosts, Certificate, Network
from webserver.common.permissions import PermissionViewMixin
from webserver.AuthManage.models import Authorize
from webserver.BusinessManage.models import Business
from webserver.UserManage.models import User


class AuthCertificateLists(LoginValidate, PermissionViewMixin, BaseView):
    """
        主机凭证列表
    """
    permission_view = "view_certificate"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', Certificate.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["msg"] = str(e)
        return info


class AuthCertificateAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑主机凭证
    """
    permission_view = "add_hosts_certificate"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            if request_data is not None:
                data = api.Api.json_load(request_data)
                if data.get("id") == "":
                    hosts = Certificate.objects.filter(name=data.get("name"))
                    if len(hosts) == 0:
                        certificate = Certificate()
                        certificate.name = data.get("name")
                        certificate.ssh_type = data.get("ssh_type")
                        certificate.ssh_port = int(data.get("ssh_port"))
                        certificate.ssh_user = data.get("ssh_user")
                        if data.get("ssh_type") == "KEY":
                            if data.get("ssh_key"):
                                certificate.ssh_key = data.get("ssh_key")
                            else:
                                info["msg"] = "SSH KEY不能为空！"
                                return info
                        else:
                            certificate.ssh_password = data.get("ssh_password")
                        certificate.save()
                        info["code"] = True
                    else:
                        info["msg"] = "此{0}凭证名称已存在！".format(data.get("name"))
                else:
                    ssh_password, ssh_key = "", ""
                    if data.get("ssh_type") == "KEY":
                        if data.get("ssh_key"):
                            ssh_key = data.get("ssh_key")
                        else:
                            info["msg"] = "SSH KEY不能为空！"
                            return info
                    else:
                        ssh_password = data.get("ssh_password")
                    Certificate.objects.filter(id=int(data.get("id"))).update(
                        name=data.get("name"),
                        ssh_type=data.get("ssh_type"),
                        ssh_port=int(data.get("ssh_port")),
                        ssh_user=data.get("ssh_user"),
                        ssh_key=ssh_key,
                        ssh_password=ssh_password
                    )
                    info["code"] = True
            else:
                info["msg"] = "参数错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AuthCertificateDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除主机凭证
    """
    permission_view = "delete_hosts_certificate"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            Certificate.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AuthAuthorizeAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑主机授权
    """
    permission_view = "add_hosts_authorize"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            if request_data is not None:
                data = api.Api.json_load(request_data)

                console = api.Api.json_dump({
                    "ssh": True if data.get("auth_console") == "1" else False,
                    "monitor": True if data.get("auth_monitor") == "1" else False
                })

                if data.get("auth_user") is not None and data.get("auth_user") != "":
                    user = User.objects.filter(id=int(data.get("auth_user")))
                    if len(user) != 1:
                        info["msg"] = "授权用户查找失败，请稍后在下！"
                        return info
                else:
                    info["msg"] = "用户选择异常，请稍后再试!"
                    return info

                hosts, business = [], []
                if data.get("business") is not None and data.get("business") != "":
                    for b in data.get("business").split(","):
                        query_business = Business.objects.filter(name=b)
                        business.extend(query_business)
                if data.get("hosts") is not None and data.get("hosts") != "":
                    for h in data.get("hosts").split(","):
                        query_hosts = Hosts.objects.filter(hostname=h)
                        hosts.extend(query_hosts)
                if len(hosts) == 0 and len(business) == 0:
                    info["msg"] = "主机选择不能为空！"
                    return

                if data.get("id") == "":
                    auth = Authorize.objects.filter(name=data.get("name"))
                    if len(auth) == 0:
                        authorize = Authorize()
                        authorize.name = data.get("name")
                        authorize.console = console
                        authorize.comment = data.get("comment")
                        authorize.save()

                        for h in hosts:
                            authorize.hosts.add(h)
                        for b in business:
                            authorize.business.add(b)

                        authorize.user.add(user[0])
                        authorize.save()
                        info["code"] = True
                    else:
                        info["msg"] = "此{0}授权名称已存在！".format(data.get("name"))
                else:
                    modify_authorize = Authorize.objects.filter(id=int(data.get("id")))
                    if len(modify_authorize) == 1:
                        modify_authorize.update(
                            name=data.get("name"),
                            console=console,
                            comment=data.get("comment")
                        )
                        modify_authorize[0].user.clear()
                        modify_authorize[0].business.clear()
                        modify_authorize[0].hosts.clear()

                        for h in hosts:
                            modify_authorize[0].hosts.add(h)
                        for b in business:
                            modify_authorize[0].business.add(b)

                        modify_authorize[0].user.add(user[0])
                        modify_authorize[0].save()
                        info["code"] = True
                    else:
                        info["msg"] = "主机授权查找出错，请稍后再试！"
            else:
                info["msg"] = "参数错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AuthAuthorizeDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除主机授权
    """
    permission_view = "delete_hosts_authorize"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            Authorize.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info
