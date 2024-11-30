#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from .view import timer

app_name = 'task'

urlpatterns = [
   url(r'^task/timer/lists/', timer.TaskTimerLists.as_view())
]
