#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from .view import alarm

app_name = 'alarm'

urlpatterns = [
   url(r'^alarm/rule/lists/', alarm.AlarmRuleList.as_view()),
   url(r'^alarm/application/lists/', alarm.AlarmApplicationList.as_view()),
   url(r'^alarm/route/lists/', alarm.AlarmRouteList.as_view()),
]
