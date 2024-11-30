#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from .view import recycle

app_name = 'system'

urlpatterns = [
   url(r'^recycle/lists/', recycle.RecycleViewList.as_view()),
]
