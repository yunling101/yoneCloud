#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^task/timer/lists/$", views.TaskTimerLists.as_view()),
    url(r"^task/timer/add/$", views.TaskTimerAdd.as_view()),
    url(r"^task/timer/delete/$", views.TaskTimerDelete.as_view()),
    url(r"^task/timer/detail/ids/(\d+)", views.TaskTimerDetail.as_view()),
]
