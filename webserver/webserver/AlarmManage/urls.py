#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r"^alarm/rule/$", views.AlarmRuleView.as_view()),

    url(r"^alarm/rule/add/$", views.AlarmRuleAdd.as_view()),
    url(r"^alarm/rule/delete/$", views.AlarmRuleDelete.as_view()),
    url(r"^alarm/rule/label/$", views.AlarmRuleLabel.as_view()),
    url(r"^alarm/rule/group/$", views.AlarmRuleGroup.as_view()),

    url(r"^alarm/template/$", views.AlarmTemplateCfg.as_view()),

    url(r"^alarm/route/$", views.AlarmRouteList.as_view()),
    url(r"^alarm/route/add/$", views.AlarmRouteAdd.as_view()),
    url(r"^alarm/route/delete/$", views.AlarmRouteDelete.as_view()),

    url(r"^alarm/global/config/$", views.AlarmGlobalConfigs.as_view()),
    url(r"^default_alertmanager_config/$", views.AlarmDefaultConfig.as_view()),
    url(r"^alarm/config/$", views.AlarmConfigs.as_view()),

    url(r"^alarm/application/add/$", views.AlarmApplicationAdd.as_view()),
    url(r"^alarm/application/delete/$", views.AlarmApplicationDelete.as_view()),

    url(r"^monitor/config", views.MonitorConfig.as_view()),
]
