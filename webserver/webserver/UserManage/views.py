#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.views.generic import View
from webserver.common import api
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from webserver.common.views import LoginValidate, BaseView
from webserver.UserManage.models import User, Role, Permission, White
from django.core.serializers import serialize
from django.db.models import Q
from webserver.website.lang.zh_ch import Lang
from webserver.common.permissions import PermissionViewMixin
from webserver.website.models import Rule
from webserver.common.record import Record
from webserver.SystemManage.models import Config


class Login(View):
    """
        用户登录
    """
    @method_decorator(api.ajax_http)
    def post(self, request):
        info = {"ret": False, "msg": ""}
        try:
            if "HTTP_X_FORWARDED_FOR" in request.META:
                client_ip = request.META["HTTP_X_FORWARDED_FOR"]
            else:
                client_ip = request.META["REMOTE_ADDR"]
            black = Config.objects.filter(ename="basic")
            if len(black) == 1:
                black_list, white = "", False
                for line in api.Api.json_load(black[0].config):
                    if line.get("ename") == "forbiddenip":
                        black_list = line.get("value")
                    elif line.get("ename") == "white":
                        white = True if line.get("value") == "1" else False

                for h in black_list.split("\n"):
                    if h == client_ip:
                        info["msg"] = "客户端IP已被限制登录，请联系管理员！"
                        return info

                if white:
                    white_obj = White.objects.filter(ip=client_ip)
                    if len(white_obj) == 0:
                        info["msg"] = "客户端IP已被限制登录，请联系管理员！"
                        return info

            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            user = authenticate(username=username, password=password)
            if user is not None:
                if username is not None and password is not None:
                    if user.is_active:
                        login(request, user)
                        Record.login_records(request, username, "WEB", None)
                        request.session["username"] = username
                        request.session.set_expiry(None)
                        info["ret"] = True
                    else:
                        info["msg"] = "用户已被禁用！"
                else:
                    info["msg"] = "用户名或密码错误！"
            else:
                info["msg"] = "用户名或密码错误！"
        except Exception as e:
            info["msg"] = "未知异常错误！"
            api.logger.error("{0}".format(str(e)))
        return info


class LoginOut(View):
    """
        用户登出
    """
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect("/login/")


class UserLists(LoginValidate, PermissionViewMixin, BaseView):
    """
        用户列表
    """
    permission_view = "view_user"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        request_super = request.GET.get("super", None)
        try:
            if request_super is not None and request_super == "false":
                data = serialize('json', User.objects.filter(is_superuser=False).order_by('-id'))
            else:
                data = serialize('json', User.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                if sd.get("role") is not None:
                    try:
                        role = Role.objects.get(id=int(sd.get("role"))).name
                    except:
                        role = ""
                else:
                    role = ""
                sd["role"] = role
                sd.pop("password")
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["content"] = str(e)
        return info


class UserAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑用户
    """
    permission_view = "add_user"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            if data.get("id") == "":
                user = User.objects.filter(Q(username=data["username"]) | Q(email=data["email"]))
                if len(user) == 0:
                    data.pop("id")
                    data["sid"] = api.Api.get_sid(6)
                    data["is_active"] = True if data["is_active"] == "true" else False
                    data["role"] = None if data["role"] == "" else int(data["role"])
                    User.objects.create_user(**data)
                    info["code"] = True
                else:
                    info["msg"] = "用户名或邮箱地址已存在！"
            else:
                User.objects.filter(id=int(data.get("id"))).update(
                    username=data.get("username"),
                    nickname=data.get("nickname"),
                    email=data.get("email"),
                    is_active=True if data["is_active"] == "true" else False,
                    role_id=None if data["role"] == "" else int(data["role"])
                )
                info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class UserDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        用户删除
    """
    permission_view = "delete_user"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            User.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class UserChangePassword(BaseView):
    """
        修改密码
    """
    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            if request.user.check_password(data.get("oldpassword")):
                if len(data.get("newpassword1")) < 6:
                    info["msg"] = "密码不能小于6位！"
                    return info
                if data.get("newpassword1") != data.get("newpassword2"):
                    info["msg"] = "两次密码不一致！"
                    return info
                request.user.set_password(data.get("newpassword1"))
                request.user.save()
                info["code"] = True
            else:
                info["msg"] = "原密码验证错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class UserRole(LoginValidate, PermissionViewMixin, BaseView):
    """
        角色列表
    """
    permission_view = "view_role"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', Role.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["content"] = str(e)
        return info


class UserRoleAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        角色/编辑添加
    """
    permission_view = "add_role"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            if request_data is not None:
                permission_select = []
                data = api.Api.json_load(request_data)
                if data.get("menu") is not None:
                    menu_select = [m for m in data.get("menu").split(",")]

                    if data.get("permission") is None:
                        for item in menu_select:
                            perm = Permission.objects.filter(menu=item)
                            if len(perm) == 1:
                                permission_select.append(perm[0])
                    else:
                        for p in data.get("permission").split(","):
                            item = p.split("|")
                            if len(item) == 2:
                                if item[0] not in menu_select:
                                    name = item[1].strip("/编辑")
                                    perm = Permission.objects.filter(name=name)
                                    if len(perm) == 1:
                                        permission_select.append(perm[0])
                        for n in menu_select:
                            if n not in permission_select:
                                perm = Permission.objects.filter(menu=n)
                                for p in perm:
                                    permission_select.append(p)

                if data.get("id") == "":
                    if data.get("name") == "":
                        info["msg"] = "角色名称不能为空！"
                        return info
                    perm = Role.objects.filter(name=data["name"])
                    if len(perm) == 0:
                        role = Role()
                        role.name = data.get("name")
                        role.comment = data.get("comment")
                        role.save()

                        role.permission.set(permission_select)
                        role.save()
                        info["code"] = True
                    else:
                        info["msg"] = "角色名称已存在！"
                else:
                    Role.objects.filter(id=data["id"]).update(
                        name=data.get("name"),
                        comment=data.get("comment")
                    )

                    role = Role.objects.get(id=data["id"])
                    role.permission.set(permission_select)
                    role.save()
                    # if data.get("permission") is not None:
                    #     for i in role.permission.all():
                    #         role.permission.remove(i)
                    #     for ids in data.get("permission"):
                    #         permission = Permission.objects.filter(id=int(ids))
                    #         if permission:
                    #             role.permission.add(permission[0])
                    info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class UserRoleDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        角色删除
    """
    permission_view = "delete_role"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            Role.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class UserRolePerm(BaseView):
    """
        角色权限
    """
    # permission_view = "view_role_perm"

    def get(self, request):
        info = {"code": False, "msg": "", "rows": []}
        try:
            rule = Rule.objects.filter(pid=0).order_by("id")
            for menu in rule:
                title, result = menu.title.strip(), {}
                if title == "仪表盘":
                    result["menu"] = title
                    result["child"] = []
                    result["id"] = 15
                    info["rows"].append(result)
                else:
                    permission = Permission.objects.filter(menu=title)
                    if len(permission) != 0:
                        result["menu"] = title
                        # haschild = Rule.objects.filter(pid=int(menu.id)).order_by("id")
                        child_perm = []
                        # for has in haschild:
                        #     child = has.title.strip("&nbsp;├ ")
                        #     perm_child = Permission.objects.filter(name=child)
                        #     if len(perm_child) != 0:
                        for has in permission:
                            name = has.name + "/编辑" if "添加" in has.name else has.name
                            child_perm.append({"menu": name, "id": has.id})
                        result["child"] = child_perm
                        info["rows"].append(result)

            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class UserPerm(LoginValidate, PermissionViewMixin, BaseView):
    """
        权限列表
    """
    permission_view = "view_permission"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', Permission.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["content"] = str(e)
        return info


class UserPermAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        权限/编辑添加
    """
    permission_view = "add_permission"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            if request_data is not None:
                data = api.Api.json_load(request_data)
                if data.get("id") == "":
                    perm = Permission.objects.filter(name=data["name"])
                    if len(perm) == 0:
                        permission = Permission()
                        permission.name = data.get("name")
                        permission.menu = data.get("menu")
                        permission.view = data.get("view")
                        permission.comment = data.get("comment")
                        permission.save()
                        info["code"] = True
                    else:
                        info["msg"] = "权限名已存在！"
                else:
                    Permission.objects.filter(id=data["id"]).update(
                        name=data.get("name"),
                        menu=data.get("menu"),
                        view=data.get("view"),
                        comment=data.get("comment")
                    )
                    info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class UserPermDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        权限删除
    """
    permission_view = "delete_permission"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            Permission.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class WhiteLists(LoginValidate, PermissionViewMixin, BaseView):
    """
        登录白名单列表
    """
    permission_view = "view_white"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', White.objects.all().order_by('-id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["content"] = str(e)
        return info


class WhiteAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        登录白名单/编辑添加
    """
    permission_view = "add_white"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            username = request.user.username
            netmask = "255.255.255.255"
            if request_data is not None:
                data = api.Api.json_load(request_data)
                if data.get("id") == "":
                    black = White.objects.filter(ip=data["address"])
                    if len(black) == 0:
                        white = White()
                        white.ip = data.get("address")
                        white.username = username
                        white.netmask = netmask
                        white.comment = data.get("comment")
                        white.save()
                        info["code"] = True
                    else:
                        info["msg"] = "权限名已存在！"
                else:
                    White.objects.filter(id=data["id"]).update(
                        ip=data.get("name"),
                        username=username,
                        netmask=netmask,
                        comment=data.get("comment")
                    )
                    info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class WhiteDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
       登录白名单删除
    """
    permission_view = "delete_white"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            White.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info
