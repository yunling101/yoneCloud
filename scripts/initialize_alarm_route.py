#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.AlarmManage.models import AlarmRoute, AlarmConfig
from webserver.defaultConfig.alertmanager import default_manager_config


def main():
    name = "default"
    if AlarmRoute.objects.filter(name=name).exists() is False:
        route, created = AlarmRoute.objects.get_or_create(
            name=name,
            group_by="alertname",
            group_wait="30s",
            group_interval="300s",
            repeat_interval="2h",
            match=""
        )
        if created:
            print("AlarmRoute insert success: {0}".format(route.id))
            webhook_configs = json.dumps([default_manager_config["webhook_configs"]])
            email_configs = json.dumps([default_manager_config["email_configs"]])
            wechat_configs = json.dumps([default_manager_config["wechat_configs"]])
            cfg_list = [
                {'id': 1, 'cname': '', 'ename': 'webhook_configs', 'config': f'{webhook_configs}', 'route_id': route.id},
                {'id': 2, 'cname': '', 'ename': 'email_configs', 'config': f'{email_configs}', 'route_id': route.id},
                {'id': 3, 'cname': '', 'ename': 'wechat_configs', 'config': f'{wechat_configs}', 'route_id': route.id},
            ]
            for c in cfg_list:
                cfg, exists = AlarmConfig.objects.get_or_create(**c)
                if exists:
                    print("AlarmConfig insert success: {0}".format(cfg.id))
                else:
                    print("AlarmConfig insert already exists")
    else:
        print("AlarmRoute insert already exists")


if __name__ == "__main__":
    main()
