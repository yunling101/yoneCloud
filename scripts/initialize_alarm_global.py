#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.AlarmManage.models import AlarmGlobalConfig


def main():
    email_config = json.dumps([
        {"cname": "开启", "ename": "enabled", "value": "0"},
        {"cname": "服务器", "ename": "server", "value": ""},
        {"cname": "用户名", "ename": "username", "value": ""},
        {"cname": "密码", "ename": "password", "value": ""},
        {"cname": "端口", "ename": "port", "value": "25"},
        {"cname": "报警模板", "ename": "template", "value": "0"}
    ])
    weixin_config = json.dumps([
        {"cname": "开启", "ename": "enabled", "value": "0"},
        {"cname": "企业ID", "ename": "corp_id", "value": ""},
        {"cname": "应用ID", "ename": "agent_id", "value": ""},
        {"cname": "应用凭证", "ename": "api_secret", "value": ""},
        {"cname": "报警模板", "ename": "template", "value": "0"}
    ])
    queryset = [
        {'id': 1, 'cname': '邮件配置', 'ename': 'email', 'config': f'{email_config}'},
        {'id': 2, 'cname': '企业微信', 'ename': 'weixin', 'config': f'{weixin_config}'},
    ]

    for cfg in queryset:
        config, created = AlarmGlobalConfig.objects.get_or_create(**cfg)
        if created:
            print("AlarmGlobalConfig insert success: " + str(config.id))
        else:
            print("AlarmGlobalConfig insert already exists")


if __name__ == "__main__":
    main()
