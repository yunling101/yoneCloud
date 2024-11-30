#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.UserManage.models import User
from webserver.ResourceManage.models import Hosts, Certificate
from webserver.BusinessManage.models import Business, Cluster
from webserver.common import api
from webserver.AuditManage.models import Login, Option
from webserver.EventManage.models import Event
from django.core.serializers import serialize
from functools import reduce
from webserver.SystemManage.models import Config
from webserver.settings import RDS
from .sender import SenderMail
from .permissions import UserAuthorize
from operator import itemgetter


class IndexView(object):
    @classmethod
    def stat(cls):
        user = User.objects.all()
        hosts = Hosts.objects.all()
        business = Business.objects.all()
        cluster = Cluster.objects.all()
        line = Config.objects.filter(ename="basic")

        auth_type, auth_version = "未知", "unknown"
        if len(line) == 1:
            for cfg in api.Api.json_load(line[0].config):
                if cfg.get("ename") == "auth_type":
                    auth_type = cfg["value"]
                elif cfg.get("ename") == "version":
                    auth_version = cfg["value"]

        return {
            "user": user.count(),
            "hosts": hosts.count(),
            "business": business.count(),
            "cluster": cluster.count(),
            "time": api.Api.sftime(),
            "auth_type": auth_type,
            "auth_version": auth_version
        }

    @classmethod
    def week(cls):
        info = {"code": False, "msg": {"labels": [], "datasets": []}, "hosts": "", "business": ""}
        hosts_data, business_data = [], []
        for num in range(0, 7):
            t = api.Api.number_day(-num)
            info["msg"]["labels"].append(t.strftime("%m-%d"))
            hosts = Hosts.objects.filter(create_time__range=(api.Api.start_time(t), api.Api.end_time(t)))
            busines = Business.objects.filter(create_time__range=(api.Api.start_time(t), api.Api.end_time(t)))
            hosts_data.append(len(hosts))
            business_data.append(len(busines))

        host = {
            "label": "主机",
            "backgroundColor": "#cde7f1",
            "borderColor": "#75c7e6",
            "pointBackgroundColor": "#75c7e6",
            "pointBorderColor": '#fff',
            "data": hosts_data
        }
        business = {
            "label": "业务",
            "backgroundColor": "rgba(220,220,220,0.5)",
            "borderColor": "rgba(220,220,220,1)",
            "pointBackgroundColor": "rgba(220,220,220,1)",
            "pointBorderColor": "#fff",
            "data": business_data
        }
        info["hosts"] = reduce(lambda x, y: x+y, hosts_data)
        info["business"] = reduce(lambda x, y: x + y, business_data)
        info["msg"]["datasets"].append(host)
        info["msg"]["datasets"].append(business)

        info["code"] = True
        return info

    @classmethod
    def login(cls, request):
        info = {"code": False, "data": []}
        if request.user.is_superuser:
            login = Login.objects.all().order_by("-id")[:4]
        else:
            login = Login.objects.filter(username=request.user.username).order_by("-id")[:6]
        data = serialize('json', login)
        for line in api.Api.json_load(data):
            sd = line["fields"]
            sd["id"] = line["pk"]
            info["data"].append(sd)
        info["code"] = True
        return info

    @classmethod
    def option(cls, request):
        info = {"code": False, "data": []}
        if request.user.is_superuser:
            option = Option.objects.all().order_by("-id")[:5]
        else:
            option = Option.objects.filter(username=request.user.username).order_by("-id")[:5]
        data = serialize('json', option)
        for line in api.Api.json_load(data):
            sd = line["fields"]
            sd["id"] = line["pk"]
            info["data"].append(sd)
        info["code"] = True
        return info

    @classmethod
    def event(cls):
        event = Event.objects.filter(status=True)
        return {
            "count": event.count(),
            "time": api.Api.sftime(),
        }

    @classmethod
    def monitor(cls, request, url):
        if request.user.is_superuser and url != "":
            return True
        return True if UserAuthorize(uid=request.user.id).get_monitor() and url != "" else False


class SystemConfig(object):
    @classmethod
    def is_recycle(cls):
        try:
            line = Config.objects.filter(ename="basic")
            if len(line) == 1:
                for cfg in api.Api.json_load(line[0].config):
                    if cfg.get("ename") == "recycle":
                        if cfg.get("value") == "1":
                            return True
        except Exception as e:
            api.logger.error(str(e))
        return False

    @classmethod
    def modify_logo(cls, path):
        info = {"code": False, "msg": path}
        try:
            line = Config.objects.filter(ename="basic")
            if len(line) == 1:
                config = []
                for cfg in api.Api.json_load(line[0].config):
                    if cfg.get("ename") == "logo":
                        cfg["value"] = path
                    config.append(cfg)
                line.update(config=api.Api.json_dump(config))
                info["code"] = True
                info["msg"] = path
            else:
                info["msg"] = "数据库查找错误，请稍后再试！"
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = "未知错误！"
        return info


class UserResetOption(object):
    footer = "此邮件由系统自动发出,请勿直接回复。<br> 如果在使用中遇到问题, 请联系管理员！"
    @classmethod
    def send_code(cls, email):
        info = {"code": False, "msg": ""}
        try:
            user = User.objects.filter(email=email)
            if len(user) == 1:
                code = api.Api.get_sid(6)
                RDS.set(email, code, ex=7200)
                msg = "您的验证码是 <b>{0}</b><br><br>".format(code)
                login = SenderMail.sender(email, msg + cls.footer, "邮箱验证码")
                if login.get("code"):
                    info["code"] = True
                else:
                    info["msg"] = login.get("msg")
            else:
                info["msg"] = "{0} 不存在或不是唯一！".format(email)
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = "未知错误, 请稍后再试！"
        return info

    @classmethod
    def query_code(cls, email, code):
        info = {"code": False, "msg": ""}
        try:
            user = User.objects.filter(email=email)
            if len(user) == 1:
                query_code = RDS.get(email)
                if isinstance(query_code, bytes):
                    query_code = query_code.decode()
                if query_code == code:
                    new_password = api.Api.crypt_sha512(api.Api.rand(5), api.Api.rand(1))
                    msg = "您的新登录密码是 <b>{0}</b><br><br>".format(new_password)
                    sender = SenderMail.sender(email, msg + cls.footer, "密码重置")
                    if sender.get("code"):
                        user[0].set_password(new_password)
                        user[0].save()
                        info["code"] = True
                    else:
                        info["msg"] = sender.get("msg")
                else:
                    info["msg"] = "验证码不匹配！"
            else:
                info["msg"] = "{0} 不存在或不是唯一！".format(email)
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = "未知错误, 请稍后再试！"
        return info


class ResourceOption(object):
    @classmethod
    def add_hosts(cls, obj):
        info = {"code": False, "msg": ""}
        try:
            obj["sid"] = int(api.Api.get_sid(6))
            obj["proxy"] = True if obj.get("proxy") == "1" else False
            obj["instance_id"] = obj.get("instance_id") if obj.get("instance_id") else obj.get("hostname")
            obj["status"] = api.Api.json_dump({"time": api.Api.sftime(), "status": "unknown"})

            handle_lists = ["certificate", "business"]
            certificate_name, business_name = itemgetter(*handle_lists)(obj)
            for k in handle_lists:
                obj.pop(k)

            business = Business.objects.filter(name=business_name)
            if len(business) != 1:
                business = Business.objects.filter(name="默认业务")
                if len(business) != 1:
                    business = Business.objects.none()

            certificate = Certificate.objects.filter(name=certificate_name)
            if len(certificate) != 1:
                certificate = Certificate.objects.filter(name="默认凭证")
                if len(certificate) != 1:
                    certificate = Certificate.objects.none()
            hosts = Hosts(**obj)
            hosts.save()

            for c in certificate:
                hosts.certificate.add(c)
            for b in business:
                hosts.business.add(b)
            hosts.save()
            info["code"] = True
        except Exception as e:
            api.logger.error(str(e))
            info["msg"] = "未知错误, 请稍后再试！"
        return info


class WebSocketAuth(object):
    # 权限验证
    def has_permission(self, username, ip):
        return False
