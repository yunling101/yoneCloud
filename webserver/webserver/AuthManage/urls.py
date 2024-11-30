#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^auth/certificate/lists/$", views.AuthCertificateLists.as_view()),
    url(r"^auth/certificate/add/$", views.AuthCertificateAdd.as_view()),
    url(r"^auth/certificate/delete/$", views.AuthCertificateDelete.as_view()),

    url(r"^auth/authorize/add/$", views.AuthAuthorizeAdd.as_view()),
    url(r"^auth/authorize/delete/$", views.AuthAuthorizeDelete.as_view()),
]
