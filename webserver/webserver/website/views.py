#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .lang.zh_ch import Lang, get_language
from .common import load_index_config, load_navigation_memu

from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.shortcuts import render
from django.core.serializers import serialize

from webserver.website.models import Rule
from webserver.common import api, monitor
from webserver.common.utils import IndexView, SystemConfig, UserResetOption
from webserver.settings import CTR_ADDRESS, WORKDIR
from webserver.common.permissions import PermissionViewMixin
from webserver.common.views import LoginValidate, BaseView
from webserver.UserManage.permissions import query_user_permission
from django.http import HttpResponse, HttpResponseRedirect


@method_decorator(api.validate_logon, name="dispatch")
class Index(View):
    """
        首页
    """
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        query_config = load_index_config()
        if query_config["code"]:
            english = True if query_config["msg"].get("language") == "english" else False
            query_menu = load_navigation_memu(request, english)
            response_data = {
                "menu": query_menu,
                "language": query_config["msg"].get("language"),
                "config": query_config["msg"],
                "lang": {
                    "menu": Lang.get("MENU"),
                    "visualization": Lang.get("Monitor Dashboard"),
                    "view": Lang.get("View All"),
                    "logout": Lang.get("Log out"),
                    "changepassword": Lang.get("Change Password"),
                    "message": Lang.get("You have {0} messages").format(IndexView.event().get("count")),
                    "login": Lang.get("Welcome {0}").format(request.user.username),
                    "extension": Lang.get("EXTRA"),
                },
                "event": IndexView.event(),
                "year": api.datetime.datetime.now().year,
            }
            cfg = monitor.Cfg.get("grafana")
            if cfg.get("link") == "true":
                response_data["monitor"] = {
                    "url": cfg["address"],
                    "status": IndexView.monitor(request, cfg["address"])
                }
            return render(request, self.template_name, response_data)
        return HttpResponse(api.Api.json_dump(query_config), content_type="application/json")


class Login(View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        query_config = load_index_config()
        if query_config["code"]:
            return render(request, self.template_name, {
                "config": query_config["msg"],
                "year": api.datetime.datetime.now().year,
                "lang": {
                    "forgot": Lang.get("forgot password"),
                    "remember": Lang.get("remember password"),
                    "email": Lang.get("email"),
                    "username": Lang.get("username"),
                    "password": Lang.get("password"),
                    "login": Lang.get("sign in"),
                }
            })
        return HttpResponse(query_config, content_type="application/json")


class ForgotCode(View):
    """
        忘记密码验证码
    """
    def post(self, request):
        info = {"code": False, "msg": ""}
        request_email = request.POST.get("email", None)
        try:
            if request_email is not None:
                info = UserResetOption.send_code(request_email)
            else:
                info["msg"] = Lang.get("unknown exception error")
        except Exception as e:
            info["msg"] = str(e)
        return HttpResponse(api.Api.json_dump(info), content_type="application/json")


class ForgotPassword(View):
    template_name = "forgot.html"

    def get(self, request, *args, **kwargs):
        query_config = load_index_config()
        if query_config["code"]:
            return render(request, self.template_name, {
                "config": query_config["msg"],
                "year": api.datetime.datetime.now().year,
                "lang": {
                    "name": Lang.get("forgot password"),
                    "email": Lang.get("email"),
                    "code": Lang.get("code"),
                    "get": Lang.get("get"),
                    "login": Lang.get("login"),
                }
            })
        return HttpResponse(query_config, content_type="application/json")

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_email = request.POST.get("email", None)
        request_code = request.POST.get("code", None)
        try:
            if request_email is not None and request_code is not None:
                vaild = UserResetOption.query_code(request_email, request_code)
                if vaild.get("code"):
                    info["msg"] = "密码发送成功, 请查收邮件！"
                    info["code"] = True
                else:
                    info["msg"] = vaild.get("msg")
            else:
                info["msg"] = "参数错误, 请稍后在试下！"
        except Exception as e:
            api.logger.error("{0}".format(str(e)))
            info["msg"] = Lang.get("unknown exception error")
        return HttpResponse(api.Api.json_dump(info), content_type="application/json")


class AuthRuleList(LoginValidate, PermissionViewMixin, BaseView):
    """
        菜单规则列表
    """
    permission_view = "view_rule"
    operation_record = False

    def get(self, request, *args, **kwargs):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        sort = request.GET.get("sort", "weigh")
        try:
            data = serialize('json', Rule.objects.all().order_by(sort))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            info["msg"] = str(e)
        return info


class AuthRuleAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑菜单规则
    """
    permission_view = "add_rule"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            spacer = ""
            if data["pid"] != "0":
                spacer = "&nbsp;├"

            menu = Rule.objects.filter(id=int(data["pid"]))
            if data["pid"] == "0" and len(menu) != 0:
                haschild = True
            else:
                if len(menu) == 1 and menu[0].pid != 0:
                    spacer = "&nbsp;|&nbsp;├"
                    menu.update(haschild=True)
                haschild = False

            if data.get("id") == "":
                rule = Rule.objects.filter(name=data["name"])
                if len(rule) == 0:
                    rule = Rule()
                    rule.name = data["name"]
                    rule.title = data["title"]
                    rule.entile = data["entitle"]
                    rule.icon = data["icon"]
                    rule.comment = data["remark"]
                    rule.ismenu = True if data["ismenu"] == "1" else False
                    rule.condition = data["condition"]
                    rule.weigh = int(data["weigh"])
                    rule.pid = int(data["pid"])
                    rule.priority = int(data["priority"])
                    rule.haschild = haschild
                    rule.status = True if int(data["status"]) == 1 else False
                    rule.spacer = spacer
                    rule.save()
                    info["code"] = True
                else:
                    info["msg"] = "名称已存在！"
            else:
                Rule.objects.filter(id=(data["id"])).update(
                    name=data["name"],
                    title=data["title"],
                    entitle=data["entitle"],
                    icon=data["icon"],
                    comment=data["remark"],
                    ismenu=True if data["ismenu"] == "1" else False,
                    condition=data["condition"],
                    weigh=int(data["weigh"]),
                    pid=int(data["pid"]),
                    priority=int(data["priority"]),
                    haschild=haschild,
                    status=True if int(data["status"]) == 1 else False,
                    spacer=spacer
                )
                info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AuthRuleDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        菜单规则删除
    """
    permission_view = "delete_rule"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            Rule.objects.filter(id=int(request_id)).delete()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AuthRuleChange(LoginValidate, PermissionViewMixin, BaseView):
    """
        菜单规则修改
    """
    permission_view = "change_rule"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        request_params = request.POST.get("params", None)
        try:
            if request_id is not None and request_params is not None:
                params = request_params.split("=")
                if len(params) == 2:
                    if params[1] == "0":
                        menu = False
                    else:
                        menu = True
                    Rule.objects.filter(id=int(request_id)).update(
                        ismenu=menu
                    )
                    info["code"] = True
            else:
                info["msg"] = Lang.get("unknown exception error")
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class IndexStat(BaseView):
    """
        仪表盘统计
    """
    def get(self, request):
        info = {"code": False, "msg": ""}
        try:
            info["code"] = True
            info["msg"] = IndexView.stat()
            # if not request.user.is_superuser:
            #     info["event"] = IndexView.event(request)
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class IndexLogin(BaseView):
    """
        仪表盘登录记录
    """
    def get(self, request):
        info = {"code": False, "msg": ""}
        try:
            login = IndexView.login(request)
            if login.get("code"):
                info["msg"] = login["data"]
                info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class IndexOption(BaseView):
    """
        仪表盘操作记录
    """

    def get(self, request):
        info = {"code": False, "msg": ""}
        try:
            login = IndexView.option(request)
            if login.get("code"):
                info["msg"] = login["data"]
                info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class IndexWeek(BaseView):
    """
        仪表盘近7天数据
    """

    def get(self, request):
        info = {"code": False, "msg": ""}
        try:
            info = IndexView.week()
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class IndexCheckUpdate(BaseView):
    """
        检查更新
    """
    def post(self, request):
        info = {"code": False, "msg": ""}
        try:
            info["code"] = True
            info["msg"] = Lang.get("Already latest")
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class OauthAuthorize(BaseView):
    """
        获取监控权限
    """
    def get(self, request):
        request_username = request.user.username
        request_id = request.user.id
        info = {"code": False, "msg": ""}
        try:
            request_data = {
                "data": api.Api.json_dump({
                    "id": request_id,
                    "username": request_username
                })
            }
            request = api.requests.post("{0}/token".format(CTR_ADDRESS), data=request_data, timeout=5)
            response_data = api.Api.json_load(request.text)
            if response_data.get("code") == 1:
                info["msg"] = response_data.get("data")
                info["code"] = True
            else:
                info["msg"] = response_data.get("message")
        except Exception as e:
            info["msg"] = str(e)
        return info


class LogoUpload(BaseView):
    """
        上传(改变)Logo文件
    """
    def post(self, request):
        info = {"code": False, "msg": ""}
        request_files = request.FILES.get("data", None)
        try:
            if request_files is not None:
                logo_path = "public/static/img/"
                logo_dir = "{0}/{1}".format(WORKDIR, logo_path)
                if api.Api.path_exists(logo_dir):
                    filename = "{0}/logo_fixed.png".format(logo_dir)
                    with open(filename, "wb+") as f:
                        for chunk in request_files.chunks():
                            f.write(chunk)
                        f.close()
                    info = SystemConfig.modify_logo("/{0}logo_fixed.png".format(logo_path))
                else:
                    info["msg"] = "读取目录错误, 请稍后再试！"
            else:
                info["msg"] = "读取文件错误, 请稍后再试！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class LogoDefault(BaseView):
    """
        恢复默认Logo文件
    """
    def post(self, request):
        info = {"code": False, "msg": ""}
        try:
            logo_path = "/public/static/img/logo.png"
            info = SystemConfig.modify_logo(logo_path)
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class SSHConnect(PermissionViewMixin, TemplateView):
    """
        主机连接
    """
    permission_view = "hosts_connect"
    template_name = "ssh.html"
    raise_exception = False
    operation_record = False

    def get_context_data(self, *args, **kwargs):
        hostname = self.request.GET.get("hostname", None)
        if hostname is None:
            hostname = self.args[0]
        context = super(SSHConnect, self).get_context_data(**kwargs)
        context["id"] = int(self.args[0])
        context["hostname"] = hostname
        return context


class UserPermission(BaseView):
    """
        用户权限
    """
    def get(self, request):
        info = {"code": False, "msg": "", "data": [], "super": request.user.is_superuser}
        try:
            if request.user.is_superuser:
                info["code"] = True
            else:
                permission = query_user_permission(request.user.role_id)
                if permission.get("ret"):
                    info["data"] = permission["data"]
                    info["code"] = True
                else:
                    api.logger.error(permission.get("msg"))
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class Language(View):
    def get(self, request):
        controller = request.GET.get("controller", None)
        if controller == "index":
            pass
        response = HttpResponse(api.Api.json_dump(get_language(), ensure_ascii=False))
        response["Content-Type"] = "application/json"
        response["Cache-Control"] = "public"
        response["Pragma"] = "cache"
        return response
