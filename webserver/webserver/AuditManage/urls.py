#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^audit/login", views.AuditLogin.as_view()),
    url(r"^audit/option", views.AuditOption.as_view()),

    url(r"^audit/detail/command/ids/(\d+)", views.AuditDetailCommand.as_view()),
    url(r"^audit/detail/playback/ids/(\d+)", views.AuditDetailPlayback.as_view())
]
