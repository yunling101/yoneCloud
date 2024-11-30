#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import jwt
from webserver.common import api
from webserver.website.lang.zh_ch import Lang
from webserver.AlarmManage.models import AlarmGlobalConfig
from webserver.common import monitor


alertmanager_config_global_mail = ["smtp_from", "smtp_smarthost", "smtp_auth_username", "smtp_auth_password"]
alertmanager_config_global_wechat = ["wechat_api_secret", "wechat_api_corp_id"]
alertmanager_config_route = ["group_by", "group_wait", "group_interval", "repeat_interval", "match"]
alertmanager_cfg = monitor.Cfg.get("alertmanager")
prometheus_cfg = monitor.Cfg.get("prometheus")


def access_token(secret_key):
    return jwt.encode({}, secret_key, algorithm="HS256")


class Overview(object):
    @classmethod
    def rule_delete(cls, data):
        info = {"code": False, "msg": ""}
        try:
            request_body = api.Api.json_dump({
                "groups": [{
                    "name": data.alarm_group,
                    "rules": [{
                        "alert": data.name,
                        "expr": data.expression,
                        "for": data.interval,
                        "labels": api.Api.json_load(data.tags),
                        "annotations": {
                            "summary": data.title,
                            "description": data.content
                        }
                    }]
                }]
            })
            headers = {
                "Token": access_token(prometheus_cfg.get("secret_key"))
            }
            address = "{0}/delete_rules".format(prometheus_cfg.get("plug"))
            request = requests.delete(address, data=request_body, headers=headers, timeout=5)
            response_data = api.Api.json_load(request.text)
            if response_data.get("code") == 1:
                info["code"] = True
            else:
                info["msg"] = response_data.get("message")
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    @classmethod
    def rule_add(cls, data):
        info = {"code": False, "msg": ""}
        try:
            request_body = api.Api.json_dump({
                "groups": [{
                    "name": data["group"],
                    "rules": [{
                        "alert": data["name"],
                        "expr": data["expr"],
                        "for": data["interval"],
                        "labels": data["label"],
                        "annotations": {
                            "summary": data["title"],
                            "description": data["description"]
                        }
                    }]
                }]
            })
            headers = {
                "Token": access_token(prometheus_cfg.get("secret_key"))
            }
            address = "{0}/sync_rules".format(prometheus_cfg.get("plug"))
            request = requests.post(address, data=request_body, headers=headers, timeout=5)
            response_data = api.Api.json_load(request.text)
            if response_data.get("code") == 1:
                info["code"] = True
            else:
                info["msg"] = response_data.get("message")
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    @classmethod
    def label_name(cls):
        info = {"code": False, "msg": "", "data": []}
        try:
            request = requests.get("http://{0}/api/v1/label/__name__/values".format(""), timeout=30)
            response_data = api.Api.json_load(request.text)
            if response_data.get("status") == "success":
                info["code"] = True
                info["data"] = response_data.get("data")
            else:
                info["msg"] = response_data.get("data")
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info


class AlarmCfg(object):
    """
        获取告警配置内容
    """
    @classmethod
    def query_config(cls):
        info = {"code": False, "msg": "", "data": ""}
        try:
            headers = {"Token": access_token(alertmanager_cfg.get("secret_key"))}
            request = requests.get("{0}/get_config".format(alertmanager_cfg.get("plug")), headers=headers)
            response_data = api.Api.json_load(request.text)
            if response_data.get("code") == 1:
                info["data"] = response_data.get("data")
                info["code"] = True
            else:
                info["msg"] = response_data.get("message")
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    @classmethod
    def overlay_route(cls, cfg):
        info = {"code": False, "msg": ""}
        try:
            query_data = cls.query_config()
            if query_data.get("code"):
                query_data = query_data.get("data")
            else:
                return query_data
            route_cfg = query_data.get("route")

            match = {}
            for k in cfg.get("match").split("\r\n"):
                v = k.replace(" ", "").replace("\r", "").replace("\n", "").split(":")
                if len(v) == 2:
                    match[v[0]] = v[1]
            new_cfg = {
                "group_by": cfg.get("group_by").split(","),
                "group_wait": cfg.get("group_wait"),
                "group_interval": cfg.get("group_interval"),
                "repeat_interval": cfg.get("repeat_interval")
            }
            if len(match) != 0:
                new_cfg["match"] = match
            if cfg.get("route_id") == "1":
                for field in alertmanager_config_route:
                    route_cfg[field] = new_cfg.get(field)
            else:
                routes_cfg = route_cfg.get("routes")
                if routes_cfg is not None:
                    modify = False
                    for index, route in enumerate(routes_cfg):
                        if route.get("receiver") == cfg.get("name"):
                            for field in alertmanager_config_route:
                                routes_cfg[index][field] = new_cfg.get(field)
                            modify = True
                    if modify is False:
                        new_cfg["receiver"] = cfg.get("name")
                        routes_cfg.append(new_cfg)
                else:
                    new_cfg["receiver"] = cfg.get("name")
                    routes_cfg = [new_cfg]
                route_cfg["routes"] = routes_cfg
            query_data["route"] = route_cfg
            info = cls.request(query_data)
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    @classmethod
    def delete_route(cls, name):
        """
            删除 Route 和 Receivers
        """
        info = {"code": False, "msg": ""}
        try:
            query_data = cls.query_config()
            if query_data.get("code"):
                query_data = query_data.get("data")
            else:
                return query_data

            route_cfg = query_data.get("route")
            routes_cfg = route_cfg.get("routes")
            if routes_cfg is not None:
                routes = []
                for route in routes_cfg:
                    if route.get("receiver") != name:
                        routes.append(route)
                route_cfg["routes"] = routes
            query_data["route"] = route_cfg

            receivers_cfg = query_data.get("receivers")
            if receivers_cfg is not None:
                receivers = []
                for receiver in receivers_cfg:
                    if receiver.get("name") != name:
                        receivers.append(receiver)
                query_data["receivers"] = receivers

            info = cls.request(query_data)
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    @classmethod
    def modify_global_config(cls, channel, cfg):
        info = {"code": False, "msg": ""}
        try:
            query_data = cls.query_config()
            if query_data.get("code"):
                query_data = query_data.get("data")
            else:
                return query_data

            global_cfg = query_data.get("global")
            if channel == "email":
                if cfg["enabled"] == "1":
                    mail_cfg = {
                        "smtp_from": cfg.get("username"),
                        "smtp_smarthost": "{0}:{1}".format(cfg.get("server"), cfg.get("port")),
                        "smtp_auth_username": cfg.get("username"),
                        "smtp_auth_password": cfg.get("password")
                    }
                    for field in alertmanager_config_global_mail:
                        global_cfg[field] = mail_cfg.get(field)
                else:
                    for field in alertmanager_config_global_mail:
                        global_cfg.pop(field, None)
            elif channel == "weixin":
                if cfg["enabled"] == "1":
                    wechat_cfg = {
                        "wechat_api_secret": cfg.get("api_secret"),
                        "wechat_api_corp_id": cfg.get("corp_id"),
                    }
                    for field in alertmanager_config_global_wechat:
                        global_cfg[field] = wechat_cfg.get(field)
                else:
                    for field in alertmanager_config_global_wechat:
                        global_cfg.pop(field, None)

            query_data["global"] = global_cfg
            info = cls.request(query_data)
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    @classmethod
    def conversion_config(cls, name, config):
        empty = True
        for index, value in enumerate(config):
            if value.get("send_resolved") == "1":
                config[index]["send_resolved"] = True
            else:
                config[index]["send_resolved"] = False
            for k, v in value.items():
                if k != "send_resolved" and v != "":
                    empty = False

            if empty is False:
                cfg, status = cls.template_config(name)
                if status is True:
                    for k, v in cfg.items(): config[index][k] = v
        return config, empty

    @classmethod
    def template_config(cls, name):
        status = False
        template = AlarmGlobalConfig.objects.filter(ename="email")
        config = {
            "headers": {"Subject": '{{ .CommonAnnotations.summary }}'},
            "html": '{{ template "mail.tmpl" . }}'
        }
        if name == "wechat_configs":
            template = AlarmGlobalConfig.objects.filter(ename="weixin")
            config = {"message": '{{ template "weixin.tmpl" .}}'}
        if len(template) == 1:
            configs = api.Api.json_load(template[0].config)
            for v in configs:
                if v.get("ename") == "template" and v.get("value") == "1":
                    status = True
        return config, status

    @classmethod
    def modify_receiver(cls, route_name, cfg):
        info = {"code": False, "msg": ""}
        try:
            query_data = cls.query_config()
            if query_data.get("code"):
                query_data = query_data.get("data")
            else:
                return query_data

            receivers_cfg = query_data.get("receivers")
            new_receiver = False
            for index, receiver in enumerate(receivers_cfg):
                if receiver.get("name") == route_name:
                    for v in cfg:
                        if v.get("ename") is not None:
                            config, empty = cls.conversion_config(v["ename"], v["config"])
                            if empty is False:
                                receivers_cfg[index][v["ename"]] = config
                    new_receiver = True

            if new_receiver is False:
                for v in cfg:
                    if v.get("ename") is not None:
                        config, empty = cls.conversion_config(v["ename"], v["config"])
                        if empty is False:
                            receivers_cfg.append({
                                "name": route_name,
                                v["ename"]: config
                            })

            query_data["receivers"] = receivers_cfg
            info = cls.request(query_data)
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    @classmethod
    def request(cls, query_data):
        info = {"code": False, "msg": ""}
        try:
            request_body = api.Api.json_dump(query_data)
            headers = {"Token": access_token(alertmanager_cfg.get("secret_key"))}
            address = "{0}/overlay_config".format(alertmanager_cfg.get("plug"))
            request = requests.post(address, headers=headers, data=request_body, timeout=5)
            response_data = api.Api.json_load(request.text)
            if response_data.get("code") == 1:
                info["data"] = response_data.get("data")
                info["code"] = True
            else:
                info["msg"] = response_data.get("message")
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info

    @classmethod
    def modify_template(cls, cfg):
        info = {"code": False, "msg": ""}
        try:
            request_body = api.Api.json_dump({
                "filename": cfg.get("filename"),
                "content": cfg.get("content")
            })
            headers = {
                "Token": access_token(alertmanager_cfg.get("secret_key"))
            }
            address = "{0}/alert_template".format(alertmanager_cfg.get("plug"))
            request = requests.post(address, headers=headers, data=request_body, timeout=5)
            response_data = api.Api.json_load(request.text)
            if response_data.get("code") == 1:
                info["data"] = response_data.get("data")
                info["code"] = True
            else:
                info["msg"] = response_data.get("message")
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = Lang.get("unknown exception error")
        return info
