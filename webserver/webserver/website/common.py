#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .models import Rule
from django.core.serializers import serialize
from webserver.common import api
from webserver.SystemManage.models import Config
from webserver.UserManage.permissions import query_user_menu


# 导航菜单
def load_navigation_memu(request):
    info = {"code": False, "msg": "", "rows": [], "total": ""}
    if request.user.is_superuser:
        menu_lists = serialize('json', Rule.objects.filter(pid=0).order_by("weigh"))
        for line in api.Api.json_load(menu_lists):
            sd = line["fields"]
            if sd["status"]:
                sd["title"] = sd["title"].strip("&nbsp;├ ")
                href = sd["name"].split("/")
                if len(href) == 1:
                    sd["id"] = sd["name"]
                elif len(href) > 1:
                    sd["id"] = href[0] + ''.join(map(lambda x: x.title(), href[1:]))
                if sd["pid"] == 0:
                    if sd["weigh"] == sd["priority"]:
                        sub = serialize("json", Rule.objects.filter(pid=int(line["pk"])).order_by("priority"))
                    else:
                        sub = serialize("json", Rule.objects.filter(pid=int(line["pk"])))
                    sd["sub"] = []
                    for ss in api.Api.json_load(sub):
                        sk = ss["fields"]
                        if sk["status"]:
                            sk["title"] = sk["title"].strip("&nbsp;├ ")
                            hrefs = sk["name"].split("/")
                            if len(hrefs) == 1:
                                sk["id"] = sk["name"]
                            elif len(hrefs) > 1:
                                sk["id"] = hrefs[0] + ''.join(map(lambda x: x.title(), hrefs[1:]))

                            if sk["haschild"] and sk["pid"] != 0:
                                sk["sub"] = []
                                san = serialize('json', Rule.objects.filter(pid=int(ss["pk"])))
                                for sjj in api.Api.json_load(san):
                                    sj = sjj["fields"]
                                    if sj["status"]:
                                        sj["title"] = sj["title"].strip("&nbsp;├ ")
                                        href_sj = sj["name"].split("/")
                                        if len(href_sj) == 1:
                                            sj["id"] = sj["name"]
                                        elif len(href_sj) > 1:
                                            sj["id"] = href_sj[0] + ''.join(map(lambda x: x.title(), href_sj[1:]))
                                        sk["sub"].append(sj)

                            sd["sub"].append(sk)
                info["rows"].append(sd)
    else:
        perm = query_user_menu(request.user.username)
        if perm.get("ret"):
            tmp_group = {}
            for p in perm.get("data"):
                rule = serialize('json', Rule.objects.filter(title=p.name))
                for line in api.Api.json_load(rule):
                    sd = line["fields"]
                    if sd["status"]:
                        href = sd["name"].split("/")
                        if len(href) == 1:
                            sd["id"] = sd["name"]
                        elif len(href) > 1:
                            sd["id"] = href[0] + ''.join(map(lambda x: x.title(), href[1:]))

                        if sd["pid"] != 0:
                            parent = serialize('json', Rule.objects.filter(id=int(sd["pid"])))
                            for ss in api.Api.json_load(parent):
                                sk = ss["fields"]
                                sk["sub"] = []
                                if sk["status"]:
                                    hrefs = sk["name"].split("/")
                                    if len(hrefs) == 1:
                                        sk["id"] = sk["name"]
                                    elif len(hrefs) > 1:
                                        sk["id"] = hrefs[0] + ''.join(map(lambda x: x.title(), hrefs[1:]))

                                    if sk["haschild"] and sk["pid"] != 0:
                                        sk["sub"].append(sd)
                                        p = Rule.objects.filter(id=int(sk["pid"]))
                                        if len(p) == 1 and p[0].pid == 0:
                                            if tmp_group.get(p[0].title):
                                                for index, sub in enumerate(tmp_group.get(p[0].title)["sub"]):
                                                    if sub.get("title") == sk.get("title"):
                                                        if tmp_group.get(p[0].title)["sub"][index].get("sub"):
                                                            tmp_group.get(p[0].title)["sub"][index]["sub"].append(sd)
                                                        else:
                                                            tmp_group.get(p[0].title)["sub"][index]["sub"] = [sd]
                                                        break
                                            else:
                                                tmp_group[p[0].title] = {"sub": [sk]}
                                    else:
                                        sk["sub"].append(sd)
                                        if tmp_group.get(sk["title"]):
                                            tmp_group.get(sk["title"])["sub"].append(sd)
                                        else:
                                            tmp_group[sk["title"]] = sk
                        else:
                            tmp_group[sd["title"]] = sd
            for k, v in tmp_group.items():
                info["rows"].append(v)
        else:
            api.logger.error("{0}".format(perm.get("msg")))
    return info["rows"]


# 导航菜单
def load_index_memu(request):
    result = []
    index = serialize("json", Rule.objects.filter(title="仪表盘"))
    for line in api.Api.json_load(index):
        sd = line["fields"]
        sd["id"] = sd["name"]
        result.append(sd)
    return result


# 首页配置
def load_index_config():
    info = {"code": False, "msg": ""}
    site = Config.objects.filter(ename="basic")
    if len(site) == 1:
        data = api.Api.json_load(site[0].config)
        info["msg"] = {k["ename"]: k["value"] for k in data}
        info["code"] = True
    else:
        info["msg"] = "站点配置读取出错！"
    return info
