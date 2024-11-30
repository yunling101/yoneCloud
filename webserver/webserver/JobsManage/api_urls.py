#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from .view import template, notify

app_name = 'jobs'

urlpatterns = [
    # url(r'^jobs/template/lists/', template.JobsTemplateLists.as_view()),
    # url(r'^jobs/notify/lists/', notify.JobsNotifyLists.as_view())
]
