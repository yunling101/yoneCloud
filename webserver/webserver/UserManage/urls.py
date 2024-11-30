#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^login_user/$", views.Login.as_view(), name="login"),
    url(r"^login_out/$", views.LoginOut.as_view(), name="login-out"),

    url(r"^user/lists/$", views.UserLists.as_view()),
    url(r"^user/add/$", views.UserAdd.as_view()),
    url(r"^user/delete/$", views.UserDelete.as_view()),
    url(r"^user/change/password/$", views.UserChangePassword.as_view()),

    url(r"^user/role/$", views.UserRole.as_view()),
    url(r"^user/role/add/$", views.UserRoleAdd.as_view()),
    url(r"^user/role/delete/$", views.UserRoleDelete.as_view()),
    url(r"^user/role/perm/$", views.UserRolePerm.as_view()),

    url(r"^user/perm/$", views.UserPerm.as_view()),
    url(r"^user/perm/add/$", views.UserPermAdd.as_view()),
    url(r"^user/perm/delete/$", views.UserPermDelete.as_view()),

    url(r"^white/lists/$", views.WhiteLists.as_view()),
    url(r"^white/add/$", views.WhiteAdd.as_view()),
    url(r"^white/delete/$", views.WhiteDelete.as_view()),
]
