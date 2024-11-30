#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from .view import certificate, authorize

app_name = 'auth'

urlpatterns = [
   url(r'^certificate/lists/', certificate.CertificateViewList.as_view()),
   url(r'^authorize/lists/', authorize.AuthorizeViewList.as_view())
]
