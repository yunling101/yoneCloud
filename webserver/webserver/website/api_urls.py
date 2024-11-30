#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from .view import auth

app_name = 'website'

urlpatterns = [
   url(r'^auth/rule/lists/', auth.RuleViewList.as_view()),
   # url(r'^auth/rule/create/', auth.RuleViewCreate.as_view()),
   # url(r'^auth/rule/update/(?P<pk>\d+)/', auth.RuleViewUpdate.as_view()),
   # url(r'^auth/rule/delete/(?P<pk>\d+)/', auth.RuleViewDelete.as_view())
]
