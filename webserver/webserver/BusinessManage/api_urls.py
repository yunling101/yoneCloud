#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from .view import business

app_name = 'business'

urlpatterns = [
   url(r'^business/lists/', business.BusinessViewList.as_view()),
   url(r'^business/create/', business.BusinessViewCreate.as_view()),
   url(r'^business/update/(?P<pk>\d+)/', business.BusinessViewUpdate.as_view()),
   url(r'^business/delete/(?P<pk>\d+)/', business.BusinessViewDelete.as_view())
]
