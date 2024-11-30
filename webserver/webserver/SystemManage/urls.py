#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^system/recycle/delete/", views.SystemRecycleDelete.as_view()),
    url(r"^system/recycle/destroy/", views.SystemRecycleDestroy.as_view()),
    url(r"^system/recycle/restore/", views.SystemRecycleRestore.as_view()),

    url(r"^system/config", views.SystemConfig.as_view()),
]
