#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.common.api import logger
from webserver.UserManage.models import Permission, User, Role


def query_user_menu(username):
    info = {"ret": False, "msg": "", "data": []}
    try:
        user = User.objects.filter(username=username)
        if len(user) == 1:
            if user[0].role_id is not None and user[0].role_id != "":
                role = Role.objects.filter(id=int(user[0].role_id))
                if len(role) == 1:
                    for i in role[0].permission.all():
                        info["data"].append(i)
                    info["ret"] = True
                else:
                    info["msg"] = "用户角色查找出错！"
            else:
                info["ret"] = True
        else:
            info["msg"] = "用户查找出错！"
    except Exception as e:
        info["msg"] = str(e)
    return info


def query_user_permission(rid):
    info = {"ret": False, "msg": "", "data": []}
    try:
        role = Role.objects.filter(id=rid)
        if len(role) == 1:
            for r in role[0].permission.all():
                info["data"].append(r.view)
            info["ret"] = True
        else:
            info["msg"] = "角色查找失败!"
    except Exception as e:
        info["msg"] = str(e)
    return info


def verify_permission(username, view):
    try:
        user = User.objects.filter(username=username)
        if len(user) == 1:
            if user[0].role_id is not None and user[0].role_id != "":
                role = Role.objects.filter(id=int(user[0].role_id))
                if len(role) == 1:
                    for i in role[0].permission.all():
                        if i.view == view:
                            return True
                else:
                    logger.error("用户角色查找出错！")
        else:
            logger.error("用户查找出错！")
    except Exception as e:
        logger.error("{0}".format(str(e)))
    return False
