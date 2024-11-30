#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^business/item/$", views.BusinessItem.as_view()),
    url(r"^business/add/$", views.BusinessAdd.as_view()),
    url(r"^business/delete/$", views.BusinessDelete.as_view()),
]
