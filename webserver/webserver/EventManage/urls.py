#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^event/lists/', views.EventList.as_view()),
    url(r'^event/change/', views.EventChange.as_view()),
    url(r'^event/delete/', views.EventDelete.as_view()),
    url(r"^event/detail/ids/(\d+)", views.EventDetail.as_view()),
]
