#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from .view import user, perm, role

app_name = 'user'

urlpatterns = [
   url(r'^user/lists/', user.UserViewList.as_view()),
   # url(r'^user/create/', user.UserViewCreate.as_view()),
   # url(r'^user/update/(?P<pk>\d+)/', user.UserViewUpdate.as_view()),
   # url(r'^user/delete/(?P<pk>\d+)/', user.UserViewDelete.as_view()),
   url(r'^user/change/password/(?P<pk>\d+)/', user.UserViewChangePassword.as_view()),

   url(r'^role/lists/', role.RoleViewList.as_view()),
   # url(r'^role/create/', role.RoleViewCreate.as_view()),
   # url(r'^role/update/(?P<pk>\d+)/', role.RoleViewUpdate.as_view()),
   # url(r'^role/delete/(?P<pk>\d+)/', role.RoleViewDelete.as_view()),

   url(r'^permission/lists/', perm.PermissionViewList.as_view()),
   # url(r'^permission/create/', perm.PermissionViewCreate.as_view()),
   # url(r'^permission/update/(?P<pk>\d+)/', perm.PermissionViewUpdate.as_view()),
   # url(r'^permission/delete/(?P<pk>\d+)/', perm.PermissionViewDelete.as_view())
]
