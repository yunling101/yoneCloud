#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.UserManage.models import Permission, Role


def main():
    entries = {"id": 1, "name": "默认角色", "comment": ""}
    
    permission = [
        {'id': 15, 'name': '仪表盘', 'menu': '仪表盘', 'view': 'view_dashboard', 'comment': ''},
        {'id': 20, 'name': '报警规则', 'menu': '监控报警', 'view': 'view_alarm_rule', 'comment': ''},
        {'id': 21, 'name': '添加告警规则', 'menu': '监控报警', 'view': 'add_alarm_rule', 'comment': ''},
        {'id': 22, 'name': '删除告警规则', 'menu': '监控报警', 'view': 'delete_alarm_rule', 'comment': ''},
        {'id': 23, 'name': '报警配置', 'menu': '监控报警', 'view': 'modify_alarm_config', 'comment': ''},
        {'id': 24, 'name': '事件管理', 'menu': '事件中心', 'view': 'view_event', 'comment': ''},
        {'id': 25, 'name': ' 删除事件', 'menu': '事件中心', 'view': 'delete_event', 'comment': ''},
        {'id': 26, 'name': '业务列表', 'menu': '业务管理', 'view': 'view_business', 'comment': ''},
        {'id': 27, 'name': '添加业务', 'menu': '业务管理', 'view': 'add_business', 'comment': ''},
        {'id': 28, 'name': '删除业务', 'menu': '业务管理', 'view': 'delete_business', 'comment': ''},
        {'id': 45, 'name': '批量命令', 'menu': '作业中心', 'view': 'batch_hosts', 'comment': ''},
        {'id': 46, 'name': '定时任务', 'menu': '任务管理', 'view': 'view_task_timer', 'comment': ''},
        {'id': 47, 'name': '添加定时任务', 'menu': '任务管理', 'view': 'add_task_timer', 'comment': ''},
        {'id': 48, 'name': '删除定时任务', 'menu': '任务管理', 'view': 'delete_task_timer', 'comment': ''},
        {'id': 50, 'name': '连接审计', 'menu': '安全审计', 'view': 'view_audit_connect', 'comment': ''},
        {'id': 51, 'name': '应用监控', 'menu': '监控报警', 'view': 'view_alarm_application', 'comment': ''},
        {'id': 52, 'name': '添加应用监控', 'menu': '监控报警', 'view': 'add_alarm_application', 'comment': ''},
        {'id': 53, 'name': '删除应用监控', 'menu': '监控报警', 'view': 'delete_alarm_application', 'comment': ''},
        {'id': 54, 'name': '资产列表', 'menu': '资产管理', 'view': 'view_asset', 'comment': ''},
        {'id': 55, 'name': '资产添加', 'menu': '资产管理', 'view': 'add_asset', 'comment': ''},
        {'id': 56, 'name': '资产删除', 'menu': '资产管理', 'view': 'delete_asset', 'comment': ''},
        {'id': 57, 'name': '创建实例', 'menu': '资产管理', 'view': 'create_asset_instance', 'comment': ''},
        {'id': 58, 'name': '重启实例', 'menu': '资产管理', 'view': 'restart_asset_instance', 'comment': ''},
        {'id': 59, 'name': '开启实例', 'menu': '资产管理', 'view': 'start_asset_instance', 'comment': ''},
        {'id': 60, 'name': '资产导出', 'menu': '资产管理', 'view': 'export_asset', 'comment': ''},
        {'id': 61, 'name': '资产分组', 'menu': '资产管理', 'view': 'view_asset_group', 'comment': ''},
        {'id': 62, 'name': '资产分组添加', 'menu': '资产管理', 'view': 'add_asset_group', 'comment': ''},
        {'id': 63, 'name': '资产分组删除', 'menu': '资产管理', 'view': 'delete_asset_group', 'comment': ''}
    ]
    
    role, created = Role.objects.get_or_create(**entries)
    if created:
        permission_select = []
        for perm in permission:
            view = Permission.objects.filter(view=perm["view"])
            if len(view) == 1:
                permission_select.append(view[0])
        role.permission.set(permission_select)
        role.save()
        
        print("Role insert success: " + str(role.id))
    else:
        print("Role insert already exists")

    
if __name__ == "__main__":
    main()

