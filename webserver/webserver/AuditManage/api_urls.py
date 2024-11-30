#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from .view import audit

app_name = 'audit'

urlpatterns = [
   url(r'^audit/login/', audit.LoginViewList.as_view()),
   url(r'^audit/option/', audit.OptionViewList.as_view()),
   url(r'^audit/command/', audit.CommandViewList.as_view()),
   url(r'^audit/connect/', audit.ConnectViewList.as_view())
]
