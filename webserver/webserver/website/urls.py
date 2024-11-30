#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^/", views.Index.as_view(), name="index"),
    url(r"^$", views.Index.as_view(), name="index"),
    url(r"^login/$", views.Login.as_view(), name="login"),
    url(r"^forgot/code/$", views.ForgotCode.as_view()),
    url(r"^forgot/password/$", views.ForgotPassword.as_view()),
    url(r"^lang", views.LangZh.as_view()),
    url(r"^permission/$", views.UserPermission.as_view()),
    url(r'^ssh/([0-9]+)/$', views.SSHConnect.as_view(), name="ssh"), # ([0-9]{10})

    url(r'^auth/rule/$', views.AuthRuleList.as_view()),
    url(r'^auth/add/$', views.AuthRuleAdd.as_view()),
    url(r'^auth/delete/$', views.AuthRuleDelete.as_view()),
    url(r'^auth/change/$', views.AuthRuleChange.as_view()),

    url(r'^index/stat/', views.IndexStat.as_view()),
    url(r'^index/week/', views.IndexWeek.as_view()),
    url(r'^index/option/', views.IndexOption.as_view()),
    url(r'^index/login/', views.IndexLogin.as_view()),
    url(r'^index/check/update/', views.IndexCheckUpdate.as_view()),

    url(r'^oauth/authorize/', views.OauthAuthorize.as_view()),
    url(r'^logo/upload/', views.LogoUpload.as_view()),
    url(r'^logo/default/', views.LogoDefault.as_view()),
]
