#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.SystemManage.models import Config


def main():
    version, version_type = "v0.1.0", "community"
    current_path = os.path.dirname(os.path.abspath(__file__))
    version_file = os.path.dirname(current_path) + "/VERSION"
    if os.path.exists(version_file):
        version = "v"+open(version_file, "r").read()
    basic_config = json.dumps([
        {"cname": "系统名称", "ename": "name", "value": "YoneCloud"},
        {"cname": "系统Logo", "ename": "logo", "value": "/public/static/img/logo.png"},
        {"cname": "回收站", "ename": "recycle", "value": "0"},
        {"cname": "系统语言", "ename": "language", "value": "chinese"},
        {"cname": "版本类型", "ename": "auth_type", "value": version_type},
        {"cname": "系统版本", "ename": "version", "value": version},
        {"cname": "系统时区", "ename": "timezone", "value": "Asia/Shanghai"},
        {"cname": "登录白名单", "ename": "white", "value": "0"},
        {"cname": "禁止(登录)IP", "ename": "forbiddenip", "value": ""}
    ])
    email_config = json.dumps([
        {"cname": "SMTP服务器", "ename": "server", "value": ""},
        {"cname": "SMTP端口", "ename": "", "value": "25"},
        {"cname": "发件人", "ename": "username", "value": ""},
        {"cname": "登入密码", "ename": "password", "value": ""}
    ])
    queryset = [
        {'id': 1, 'cname': '基础配置', 'ename': 'basic', 'config': f'{basic_config}'},
        {'id': 2, 'cname': '邮箱配置', 'ename': 'email', 'config': f'{email_config}'},
    ]

    for cfg in queryset:
        config, created = Config.objects.get_or_create(**cfg)
        if created:
            print("Config insert success: " + str(config.id))
        else:
            print("Config insert already exists")


if __name__ == "__main__":
    main()
