#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from webserver.common.api import Api, logger
from webserver.UserManage.permissions import verify_permission
from webserver.common.record import Record
from webserver.AuthManage.models import Authorize


class IsValidUser(permissions.IsAuthenticated, permissions.BasePermission):
    """
        Allows access to valid user, is active and not expired
    """

    def has_permission(self, request, view):
        return super(IsValidUser, self).has_permission(request, view) \
            and request.user.is_active


class IsOrgAdmin(IsValidUser):
    """
        Allows access only to superuser
    """

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return super(IsOrgAdmin, self).has_permission(request, view) and request.user.is_authenticated

        if not request.user.is_superuser:
            if not verify_permission(request.user.username, view.permission_view):
                return super(IsOrgAdmin, self).has_permission(request, view) and False

        try:
            if view.operation_record:
                Record.operation_records(request, view.__doc__.strip(), "")
        except:
            Record.operation_records(request, view.__doc__.strip(), "")

        return super(IsOrgAdmin, self).has_permission(request, view) and True


class UserAuthorize(object):
    """
        用户授权
    """
    def __init__(self, uid=None):
        self.uid = uid
        self.auth = self.query()

    def query(self):
        auth = Authorize.objects.filter(user=self.uid)
        return auth

    def get_monitor(self):
        if len(self.auth) == 1:
            console = Api.json_load(self.auth[0].console)
            if console.get("monitor"):
                return True
        return False

    def get_console(self):
        if len(self.auth) == 1:
            console = Api.json_load(self.auth[0].console)
            if console.get("ssh"):
                return True
        return False


class PermissionViewMixin(object):
    """
        权限验证
    """
    permission_view = None
    operation_record = True

    def has_permission(self, username):
        if self.permission_view is None:
            return False
        if not verify_permission(username, self.permission_view):
            return False

        return True

    def dispatch(self, request, *args, **kwargs):
        info = {"code": False, "msg": "权限拒绝, 请联系管理员！"}

        if not request.user.is_superuser:
            if not self.has_permission(request.user.username):
                return HttpResponse(Api.json_dump(info), content_type="application/json")

        if self.operation_record:
            Record.operation_records(request, self.__doc__.strip(), "")

        return super(PermissionViewMixin, self).dispatch(request, *args, **kwargs)
