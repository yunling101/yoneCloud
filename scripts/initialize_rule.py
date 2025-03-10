#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import datetime
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.website.models import Rule


def main():
    queryset = [
        {'id': 1, 'name': 'dashboard', 'title': '仪表盘', 'entitle': 'Dashboard', 'pid': 0, 'icon': 'fa fa-dashboard', 'weigh': 0, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 24, 15, 6, 42, 679759), 'comment': ''},
        {'id': 2, 'name': 'task', 'title': '任务管理', 'entitle': 'Tasks', 'pid': 0, 'icon': 'fa fa-tasks', 'weigh': 1, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': True, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 11, 14, 10, 332150), 'comment': ''},
        {'id': 4, 'name': 'task/list', 'title': '任务列表', 'entitle': 'Task List', 'pid': 2, 'icon': 'fa fa-tasks', 'weigh': 1, 'ismenu': True, 'spacer': '&nbsp;├', 'status': False, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 11, 31, 48, 684848), 'comment': ''},
        {'id': 5, 'name': 'task/jobs', 'title': '作业管理', 'entitle': 'Job Management', 'pid': 2, 'icon': 'fa fa-tasks', 'weigh': 1, 'ismenu': True, 'spacer': '&nbsp;├', 'status': False, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 13, 42, 46, 937522), 'comment': ''},
        {'id': 7, 'name': 'task/layout', 'title': '任务编排', 'entitle': 'Task Scheduling', 'pid': 2, 'icon': 'fa fa-tasks', 'weigh': 1, 'ismenu': True, 'spacer': '&nbsp;├', 'status': False, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 13, 45, 34, 807735), 'comment': ''},
        {'id': 8, 'name': 'jobs', 'title': '作业中心', 'entitle': 'Jobs', 'pid': 0, 'icon': 'fa fa-th', 'weigh': 2, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': True, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 13, 49, 41, 732254), 'comment': ''},
        {'id': 9, 'name': 'jobs/hosts', 'title': '主机连接', 'entitle': 'Host Connection', 'pid': 8, 'icon': 'fa fa-th', 'weigh': 2, 'ismenu': True, 'spacer': '&nbsp;├', 'status': False, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 13, 50, 51, 115830), 'comment': ''},
        {'id': 10, 'name': 'resources', 'title': '资产管理', 'entitle': 'Asset', 'pid': 0, 'icon': 'fa fa-th-list', 'weigh': 5, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': True, 'priority': 5, 'create_time': datetime.datetime(2020, 4, 26, 13, 52, 14, 364914), 'comment': ''},
        {'id': 11, 'name': 'resources/pool', 'title': '主机池', 'entitle': 'Host Pool', 'pid': 10, 'icon': 'fa fa-th-list', 'weigh': 5, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 1, 'create_time': datetime.datetime(2020, 4, 26, 13, 52, 48, 109061), 'comment': ''},
        {'id': 12, 'name': 'business', 'title': '业务管理', 'entitle': 'Business', 'pid': 0, 'icon': 'fa fa-list-alt', 'weigh': 6, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': True, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 13, 54, 57, 524558), 'comment': ''},
        {'id': 13, 'name': 'business/item', 'title': '业务列表', 'entitle': 'Business List', 'pid': 12, 'icon': 'fa fa-list-alt', 'weigh': 6, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 13, 55, 27, 243163), 'comment': ''},
        {'id': 14, 'name': 'event/lists', 'title': '事件中心', 'entitle': 'Event', 'pid': 0, 'icon': 'fa fa-bell', 'weigh': 7, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 13, 57, 21, 849383), 'comment': ''},
        {'id': 17, 'name': 'alarm', 'title': '监控报警', 'entitle': 'Monitor Alarm', 'pid': 0, 'icon': 'fa fa-desktop', 'weigh': 8, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': True, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 13, 59, 24, 708639), 'comment': ''},
        {'id': 18, 'name': 'alarm/rule', 'title': '报警规则', 'entitle': 'Alarm Rule', 'pid': 17, 'icon': 'fa fa-bell', 'weigh': 8, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 13, 59, 58, 123949), 'comment': ''},
        {'id': 19, 'name': 'alarm/template', 'title': '报警模板', 'entitle': 'Alarm Template', 'pid': 17, 'icon': 'fa fa-bell', 'weigh': 8, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 10, 24, 17, 34, 30, 177345), 'comment': ''},
        {'id': 22, 'name': 'user', 'title': '用户管理', 'entitle': 'User', 'pid': 0, 'icon': 'fa fa-user-circle', 'weigh': 10, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': True, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 2, 12, 492834), 'comment': ''},
        {'id': 23, 'name': 'user/lists', 'title': '用户列表', 'entitle': 'User List', 'pid': 22, 'icon': 'fa fa-user', 'weigh': 10, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 2, 45, 851611), 'comment': ''},
        {'id': 24, 'name': 'user/role', 'title': '角色管理', 'entitle': 'Role', 'pid': 22, 'icon': 'fa fa-user', 'weigh': 10, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 3, 22, 816866), 'comment': ''},
        {'id': 25, 'name': 'user/perm', 'title': '权限管理', 'entitle': 'Permission', 'pid': 22, 'icon': 'fa fa-user', 'weigh': 10, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 3, 51, 856842), 'comment': ''},
        {'id': 27, 'name': 'auth/rule', 'title': '菜单规则', 'entitle': 'Menu Rule', 'pid': 0, 'icon': 'fa fa-list-alt', 'weigh': 11, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 4, 42, 873782), 'comment': ''},
        {'id': 28, 'name': 'audit', 'title': '安全审计', 'entitle': 'Security Audit', 'pid': 0, 'icon': 'fa fa-eye', 'weigh': 12, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': True, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 5, 34, 781829), 'comment': ''},
        {'id': 29, 'name': 'audit/option', 'title': '操作记录', 'entitle': 'Operation Log', 'pid': 28, 'icon': 'fa fa-eye', 'weigh': 12, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 6, 4, 76897), 'comment': ''},
        {'id': 30, 'name': 'audit/login', 'title': '登录记录', 'entitle': 'Login History', 'pid': 28, 'icon': 'fa fa-eye', 'weigh': 12, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 6, 34, 682036), 'comment': ''},
        {'id': 31, 'name': 'system', 'title': '系统设置', 'entitle': 'System Settings', 'pid': 0, 'icon': 'fa fa-gear', 'weigh': 13, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': True, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 7, 37, 612917), 'comment': ''},
        {'id': 32, 'name': 'system/config', 'title': '系统设置', 'entitle': 'Settings', 'pid': 31, 'icon': 'fa fa-gear', 'weigh': 13, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 9, 25, 547912), 'comment': ''},
        {'id': 33, 'name': 'resources/recycle', 'title': '主机回收站', 'entitle': 'Host Recycle Bin', 'pid': 10, 'icon': 'fa fa-gear', 'weigh': 5, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 4, 'create_time': datetime.datetime(2020, 4, 27, 12, 26, 41, 727487), 'comment': ''},
        {'id': 37, 'name': 'system/white', 'title': '登录白名单', 'entitle': 'Whitelist', 'pid': 31, 'icon': 'fa fa-gear', 'weigh': 13, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 7, 31, 12, 22, 23, 360392), 'comment': ''},
        {'id': 38, 'name': 'jobs/batch', 'title': '批量命令', 'entitle': 'Batch Command', 'pid': 8, 'icon': 'fa fa-th', 'weigh': 2, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 8, 4, 12, 10, 50, 317500), 'comment': ''},
        {'id': 39, 'name': 'task/timer', 'title': '定时任务', 'entitle': 'Scheduled Tasks', 'pid': 2, 'icon': 'fa fa-tasks', 'weigh': 1, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 8, 4, 12, 12, 13, 896696), 'comment': ''},
        {'id': 40, 'name': 'certificate', 'title': '授权中心', 'entitle': 'Authorize', 'pid': 0, 'icon': 'fa fa-address-card', 'weigh': 3, 'ismenu': True, 'spacer': '', 'status': True, 'condition': '', 'haschild': True, 'priority': 0, 'create_time': datetime.datetime(2020, 8, 4, 12, 17, 17, 296043), 'comment': ''},
        {'id': 41, 'name': 'certificate/hosts', 'title': '主机凭证', 'entitle': 'Host Credential', 'pid': 40, 'icon': 'fa fa-address-card', 'weigh': 3, 'ismenu': True, 'spacer': '&nbsp;├', 'status': False, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 8, 4, 12, 22, 54, 111815), 'comment': ''},
        {'id': 43, 'name': 'resources/network', 'title': '网络设备', 'entitle': 'Network', 'pid': 10, 'icon': 'fa fa-th-list', 'weigh': 5, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 5, 'create_time': datetime.datetime(2020, 8, 17, 18, 10, 56, 362847), 'comment': ''},
        {'id': 44, 'name': 'audit/command', 'title': '命令审计', 'entitle': 'Command Audit', 'pid': 28, 'icon': 'fa fa-eye', 'weigh': 12, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 8, 25, 11, 48, 21, 909523), 'comment': ''},
        {'id': 45, 'name': 'audit/connect', 'title': '连接审计', 'entitle': 'Connection Audit', 'pid': 28, 'icon': 'fa fa-eye', 'weigh': 12, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 8, 25, 11, 48, 50, 473487), 'comment': ''},
        {'id': 46, 'name': 'authorize/hosts', 'title': '主机授权', 'entitle': 'Host Authorize', 'pid': 40, 'icon': 'fa fa-address-card', 'weigh': 3, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 8, 26, 19, 11, 44, 156828), 'comment': ''},
        {'id': 52, 'name': 'alarm/config', 'title': '报警配置', 'entitle': 'Alarm Config', 'pid': 17, 'icon': 'fa fa-bell', 'weigh': 8, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 4, 26, 14, 0, 29, 618433), 'comment': ''},
        {'id': 53, 'name': 'alarm/application', 'title': '应用监控', 'entitle': 'Application Monitor', 'pid': 17, 'icon': 'fa fa-bell', 'weigh': 8, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2020, 10, 11, 11, 50, 49, 361192), 'comment': ''},
        {'id': 54, 'name': 'jobs/template', 'title': '作业模板', 'entitle': 'Job Template', 'pid': 8, 'icon': 'fa fa-th', 'weigh': 2, 'ismenu': True, 'spacer': '&nbsp;├', 'status': False, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2021, 1, 1, 11, 34, 36, 222242), 'comment': ''},
        {'id': 55, 'name': 'jobs/notify', 'title': '通知模板', 'entitle': 'Notification Template', 'pid': 8, 'icon': 'fa fa-th', 'weigh': 2, 'ismenu': True, 'spacer': '&nbsp;├', 'status': False, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2021, 1, 1, 11, 46, 3, 246935), 'comment': ''},
        {'id': 56, 'name': 'resources/group', 'title': '主机分组', 'entitle': 'Host Group', 'pid': 10, 'icon': 'fa fa-th-list', 'weigh': 5, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 2, 'create_time': datetime.datetime(2024, 8, 6, 11, 47, 50, 685142), 'comment': ''},
        {'id': 57, 'name': 'resources/certificate', 'title': '主机凭证', 'entitle': 'Host Credential', 'pid': 10, 'icon': 'fa fa-th-list', 'weigh': 5, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 3, 'create_time': datetime.datetime(2024, 8, 6, 11, 49, 48, 815727), 'comment': ''},
        {'id': 58, 'name': 'alarm/monitor', 'title': '组件配置', 'entitle': 'Component Config', 'pid': 17, 'icon': 'fa fa-bell', 'weigh': 8, 'ismenu': True, 'spacer': '&nbsp;├', 'status': True, 'condition': '', 'haschild': False, 'priority': 0, 'create_time': datetime.datetime(2024, 8, 12, 15, 59, 27, 229473), 'comment': ''}
    ]
    
    for rule in queryset:
        n, created = Rule.objects.get_or_create(defaults={**rule}, id=rule["id"], name=rule["name"])
        if created:
            print("Rule insert success: " + str(n.id))
        else:
            print("Rule insert already exists")


if __name__ == "__main__":
    main()

