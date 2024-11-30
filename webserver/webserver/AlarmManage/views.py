#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.common import api, monitor
from django.core.serializers import serialize
from webserver.common.views import LoginValidate, BaseView
from webserver.AlarmManage.models import AlarmConfig, AlarmApplication, AlarmRule, \
    AlarmRoute, AlarmTemplate, AlarmGlobalConfig
from webserver.website.lang.zh_ch import Lang
from webserver.common.permissions import PermissionViewMixin
from webserver.defaultConfig.alertmanager import default_manager_config
from webserver.defaultConfig.prometheus import default_rule_group
from webserver.AlarmManage.utils import Overview, AlarmCfg
from webserver.ResourceManage.consuld import CC
from django.db.models import Q


class AlarmRuleView(LoginValidate, PermissionViewMixin, BaseView):
    """
        告警规则
    """
    permission_view = "view_alarm_rule"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": 0}
        ret = Overview.rules()
        if ret.get("code"):
            info["code"] = True
            info["rows"] = ret.get("data")
        else:
            info["msg"] = ret.get("msg")
        return info


class AlarmRuleAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑告警规则
    """
    permission_view = "add_alarm_rule"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            rule_name = AlarmRule.objects.filter(name=data.get("name"))
            if len(rule_name) == 0:
                rule = AlarmRule()
                rule.name = data.get("name")
                rule.expression = data.get("rules")
                rule.interval = data.get("interval")
                rule.alarm_group = data.get("group")
                rule.tags = api.Api.json_dump({"severity": data.get("level")})
                rule.title = data.get("title")
                rule.content = data.get("content")
                rule.desc = data.get("desc")
                rule.save()
            else:
                rule_name.update(
                    expression=data.get("rules"),
                    interval=data.get("interval"),
                    tags=api.Api.json_dump({"severity": data.get("level")}),
                    title=data.get("title"),
                    content=data.get("content"),
                    desc=data.get("desc")
                )
            info = Overview.rule_add({
                "group": data.get("group"),
                "name": data.get("name"),
                "interval": data.get("interval"),
                "label": {"severity": data.get("level")},
                "title": data.get("title"),
                "description": data.get("content"),
                "expr": data.get("rules")
            })
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmRuleLabel(BaseView):
    """
        Rule Label Name
    """
    def get(self, request):
        info = {"code": False, "msg": ""}
        try:
            info = Overview.label_name()
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmRuleGroup(BaseView):
    """
        Rule Group List
    """
    def get(self, request):
        return default_rule_group


class AlarmRuleDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除告警规则
    """
    permission_view = "delete_alarm_rule"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        # request_params = request.POST.get("params")
        try:
            # if request_id is not None and request_params is not None:
            if request_id is not None:
                # group_name = request_params.split("=")
                # if len(group_name) == 2:
                #     info = Overview.rule_delete(request_id, group_name[1])
                # else:
                #     info["msg"] = "参数解析出错"
                rule = AlarmRule.objects.filter(id=int(request_id))
                if len(rule) == 1:
                    info = Overview.rule_delete(rule[0])
                    if info["code"] is False:
                        return info
                rule.delete()
            else:
                info["msg"] = "参数错误"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmApplicationAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑应用监控
    """
    permission_view = "add_alarm_application"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            if request_data is not None:
                data = api.Api.json_load(request_data)
                if data.get("address") is not None and len(data["address"].split(":")) == 2:
                    hosts = data["address"].split(":")[0]
                    ports = data["address"].split(":")[1]
                else:
                    info["msg"] = "应用地址格式错误!"
                    return info

                if data.get("id") == "":
                    application = AlarmApplication.objects.filter(name=data.get("name"))
                    if len(application) == 0:
                        sid = api.Api.get_sid(8)
                        try:
                            CC().register(
                                "application",
                                sid,
                                hosts,
                                int(ports),
                                hosts,
                                "application"
                            )
                            app = AlarmApplication()
                            app.sid = int(sid)
                            app.name = data.get("name")
                            app.address = data.get("address")
                            app.comment = data.get("comment")
                            app.save()
                            info["code"] = True
                        except Exception as e:
                            api.logger.error(str(e))
                            info["msg"] = str(e)
                    else:
                        info["msg"] = "此应用名称已存在!"
                else:
                    AlarmApplication.objects.filter(id=int(data["id"])).update(
                        name=data.get("name"),
                        address=data.get("address"),
                        comment=data.get("comment")
                    )
                    info["code"] = True
            else:
                info["msg"] = "传入参数错误!"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmApplicationDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除应用监控
    """
    permission_view = "delete_alarm_application"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            if request_id is not None:
                app = AlarmApplication.objects.filter(id=int(request_id))
                try:
                    if len(app) == 1:
                        CC().deregister(str(app[0].sid))
                        app.delete()
                    info["code"] = True
                except Exception as e:
                    info["msg"] = str(e)
            else:
                info["msg"] = "传入参数错误!"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmRouteList(LoginValidate, PermissionViewMixin, BaseView):
    """
        报警路由列表
    """
    permission_view = "modify_alarm_config"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', AlarmRoute.objects.all().order_by('id'))
            for line in api.Api.json_load(data):
                sd = line["fields"]
                sd["id"] = line["pk"]
                info["rows"].append(sd)
            info["total"] = len(info["rows"])
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmRouteAdd(LoginValidate, PermissionViewMixin, BaseView):
    """
        添加/编辑报警路由
    """
    permission_view = "modify_alarm_config"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            if data.get("route_id") == "":
                routes = AlarmRoute.objects.filter(name=data.get("name"))
                if len(routes) == 0:
                    route = AlarmRoute()
                    route.name = data.get("name")
                    route.group_by = data.get("group_by")
                    route.group_wait = data.get("group_wait")
                    route.group_interval = data.get("group_interval")
                    route.repeat_interval = data.get("repeat_interval")
                    route.match = data.get("match")
                    route.save()
                    data["route_id"] = "{0}".format(route.id)
                else:
                    info["msg"] = "此路由名称已存在！"
            else:
                AlarmRoute.objects.filter(id=int(data.get("route_id"))).update(
                    name=data.get("name"),
                    group_by=data.get("group_by"),
                    group_wait=data.get("group_wait"),
                    group_interval=data.get("group_interval"),
                    repeat_interval=data.get("repeat_interval"),
                    match=data.get("match")
                )
            info = AlarmCfg.overlay_route(data)
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmRouteDelete(LoginValidate, PermissionViewMixin, BaseView):
    """
        删除报警路由
    """
    permission_view = "modify_alarm_config"

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_id = request.POST.get("ids", None)
        try:
            if request_id is not None:
                if int(request_id) != 1:
                    route = AlarmRoute.objects.filter(id=int(request_id))
                    if len(route) == 1:
                        info = AlarmCfg.delete_route(route[0].name)
                        if info.get("code"):
                            route.delete()
                            info["code"] = True
                    else:
                        info["msg"] = "路由查找不存在"
                else:
                    info["msg"] = "默认主路由不能删除"
            else:
                info["msg"] = "传入参数错误"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmGlobalConfigs(LoginValidate, PermissionViewMixin, BaseView):
    """
        全局配置
    """
    permission_view = "modify_alarm_global_config"

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', AlarmGlobalConfig.objects.all().order_by('id'))
            for line in api.Api.json_load(data):
                sline = line["fields"]
                sline["id"] = line["pk"]
                sline["config"] = api.Api.json_load(sline["config"])
                info["rows"].append(sline)
            info["code"] = True
            info["total"] = len(info["rows"])
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            config = AlarmGlobalConfig.objects.filter(ename=data["id"])
            if len(config) == 1:
                tmp_config = []
                for line in api.Api.json_load(config[0].config):
                    line["value"] = data[line["ename"]]
                    tmp_config.append(line)
                config.update(config=api.Api.json_dump(tmp_config))

                channel_cfg = {}
                for k in tmp_config:
                    channel_cfg[k["ename"]] = k["value"]

                AlarmCfg.modify_global_config(data["id"], channel_cfg)
                info["code"] = True
            else:
                info["msg"] = "配置未查询到"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmDefaultConfig(LoginValidate, BaseView):
    """
        默认配置
    """
    operation_record = False

    def get(self, request):
        return default_manager_config


class AlarmConfigs(LoginValidate, PermissionViewMixin, BaseView):
    """
        告警配置
    """
    permission_view = "modify_alarm_config"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        request_route = request.GET.get("route", None)
        try:
            if request_route is not None:
                data = serialize('json', AlarmConfig.objects.filter(route_id=int(request_route)))
                for line in api.Api.json_load(data):
                    sline = line["fields"]
                    sline["id"] = line["pk"]
                    sline["config"] = api.Api.json_load(sline["config"])
                    info["rows"].append(sline)

                info["code"] = True
                info["total"] = len(info["rows"])
            else:
                info["msg"] = "请求路由参数错误！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.body.decode()
        try:
            data = api.Api.json_load(request_data)
            route_name = ""
            for index, v in enumerate(data):
                route = AlarmRoute.objects.filter(id=int(v["route"]))
                if len(route) == 1:
                    config = AlarmConfig.objects.filter(Q(ename=v["ename"]) & Q(route_id=int(v["route"])))
                    if len(config) == 0:
                        new_config = AlarmConfig()
                        new_config.ename = v["ename"]
                        new_config.config = api.Api.json_dump(v["config"])
                        new_config.route_id = int(v["route"])
                        new_config.save()
                    else:
                        if api.Api.json_load(config[0].config) != v["config"]:
                            config.update(config=api.Api.json_dump(v["config"]))
                    route_name = route[0].name
                else:
                    info["msg"] = "路由配置查询出错"
                    return info
            if route_name == "":
                info["msg"] = "路由名称不能为空"
                return info
            info = AlarmCfg.modify_receiver(route_name, data)
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmTemplateCfg(LoginValidate, PermissionViewMixin, BaseView):
    """
        修改告警模板
    """
    permission_view = "modify_alarm_template"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": "", "rows": [], "total": ""}
        try:
            data = serialize('json', AlarmTemplate.objects.all())
            for line in api.Api.json_load(data):
                sline = line["fields"]
                sline["id"] = line["pk"]
                sline["config"] = api.Api.json_load(sline["config"])
                info["rows"].append(sline)

            info["code"] = True
            info["total"] = len(info["rows"])
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            data = api.Api.json_load(request_data)
            config = AlarmTemplate.objects.filter(ename=data.get("id"))
            if len(config) == 1:
                tmp_config = []
                for line in api.Api.json_load(config[0].config):
                    line["value"] = data[line["ename"]]
                    tmp_config.append(line)
                config.update(config=api.Api.json_dump(tmp_config))

                query_cfg = AlarmCfg.query_config()
                if query_cfg["code"]:
                    qfg = query_cfg.get("data")
                    if qfg.get("templates") is not None and len(qfg["templates"]) != 0:
                        path = api.os.path.dirname(qfg["templates"][0])
                        filename = "{0}/{1}.tmpl".format(path, data.get("id"))
                        req_tmp = AlarmCfg.modify_template({
                            "filename": filename,
                            "content": api.Api.base64(data.get("template").encode()),
                        })
                        if req_tmp["code"]:
                            info["code"] = True
                        else:
                            info["msg"] = req_tmp.get("msg")
                    else:
                        info["msg"] = "模板路径配置错误, 请检查配置文件!"
                else:
                    info["msg"] = query_cfg.get("msg")
            else:
                info["msg"] = "{0}模板不存在!".format(data.get("id"))
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class MonitorConfig(LoginValidate, PermissionViewMixin, BaseView):
    """
        监控配置
    """
    permission_view = "monitor_config"
    operation_record = False

    def get(self, request):
        info = {"code": False, "msg": ""}
        try:
            response_data = monitor.Cfg.read_all()
            if response_data is None:
                monitor.Cfg.write_default()
                response_data = monitor.Cfg.default_config
            info["msg"] = response_data
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    def post(self, request):
        info = {"code": False, "msg": ""}
        request_data = request.POST.get("data", None)
        try:
            if request_data is not None:
                new_data = api.Api.json_load(request_data)
                old_data = monitor.Cfg.read_all()
                if old_data is not None:
                    k = new_data["id"]
                    del new_data["id"]
                    old_data[k] = new_data
                    monitor.Cfg.write(old_data)
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info
