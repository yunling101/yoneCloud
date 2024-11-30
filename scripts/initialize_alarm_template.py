#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.AlarmManage.models import AlarmTemplate


def main():
    queryset = [
        {'id': 1, 'cname': '邮件模板', 'ename': 'mail', 'config': '[{"cname": "模板", "ename": "template", "value": "{{ define \\"mail.html\\" }}\\r\\n  {{ range $i, $alert := .Alerts.Firing }}\\r\\n    告警实例: {{ index $alert.Labels \\"alertname\\" }}\\r\\n    <br>\\r\\n    告警主机: {{ index $alert.Labels \\"instance\\" }}\\r\\n    <br>\\r\\n    主机名称: {{ index $alert.Labels \\"hostname\\" }}\\r\\n    <br>\\r\\n    告警时间: {{ $alert.StartsAt }}\\r\\n    <br>\\r\\n    告警描述: {{ index $alert.Annotations \\"description\\" }}\\r\\n    <br>\\r\\n    <br>\\r\\n  {{ end }}\\r\\n{{ end }}"}]'},
        {'id': 2, 'cname': '微信模板', 'ename': 'weixin', 'config': '[{"cname": "模板", "ename": "template", "value": "{{ define \\"weixin.html\\" }}\\r\\n  {{ range $i, $alert := .Alerts.Firing }}\\r\\n    [项名]:{{ index $alert.Labels \\"alertname\\" }}\\r\\n    <br>\\r\\n    [主机]:{{ index $alert.Labels \\"instance\\" }}\\r\\n    <br>\\r\\n    [阀值]:{{ index $alert.Annotations \\"value\\" }}\\r\\n    <br>\\r\\n    [时间]:{{ $alert.StartsAt }}\\r\\n  {{ end }}\\r\\n{{ end }}\\r\\n"}]'}
    ]
    
    for tpl in queryset:
        template, created = AlarmTemplate.objects.get_or_create(**tpl)
        if created:
            print("AlarmTemplate insert success: " + str(template.id))
        else:
            print("AlarmTemplate insert already exists")


if __name__ == "__main__":
    main()

