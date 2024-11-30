#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from .view import hosts, group, network

app_name = 'resource'

urlpatterns = [
   url(r'^hosts/lists/', hosts.HostsViewList.as_view()),
   url(r'^group/lists/', group.GroupViewList.as_view()),
   # url(r'^certificate/lists/', certificate.CertificateViewList.as_view()),
   url(r'^network/lists/', network.NetworkViewList.as_view())
]
