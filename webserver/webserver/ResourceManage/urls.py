#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^resources/hosts/pool/$", views.ResourcesPool.as_view()),
    url(r"^resources/hosts/add/$", views.ResourcesPoolAdd.as_view()),
    url(r"^resources/hosts/delete/$", views.ResourcesPoolDelete.as_view()),
    url(r"^resources/hosts/monitor/$", views.ResourcesPoolMonitor.as_view()),
    url(r"^resources/hosts/detail/ids/(\d+)", views.ResourcesPoolDetail.as_view()),
    url(r"^resources/hosts/upload/", views.ResourcesPoolUpload.as_view()),
    url(r"^resources/hosts/batch/$", views.ResourcesPoolBatch.as_view()),

    url(r"^resources/hosts/group/$", views.ResourcesHostsGroupAdd.as_view()),
    url(r"^resources/hosts/group/delete/$", views.ResourcesHostsGroupDelete.as_view()),

    # url(r"^resources/certificate/lists/$", views.ResourcesCertificateLists.as_view()),
    # url(r"^resources/certificate/add/$", views.ResourcesCertificateAdd.as_view()),
    # url(r"^resources/certificate/delete/$", views.ResourcesCertificateDelete.as_view()),

    url(r"^resources/network/add/$", views.ResourcesNetworkAdd.as_view()),
    url(r"^resources/network/delete/$", views.ResourcesNetworkDelete.as_view()),
    url(r"^resources/network/monitor/$", views.ResourcesNetworkMonitor.as_view()),

    url(r"^resources/provider/$", views.ResourcesProvider.as_view()),
    url(r"^resources/network_type/$", views.ResourcesNetworkType.as_view()),
]
