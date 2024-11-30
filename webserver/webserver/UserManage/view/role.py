#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.UserManage.models import Role, Permission
from webserver.common.permissions import IsOrgAdmin
from .serializers import RoleSerializer, RoleCreateSerialize
from rest_framework.response import Response

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from webserver.common.api import StandardResultsSetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from webserver.common.api import logger
from webserver.common.permissions import PermissionViewMixin


class RoleViewList(generics.ListAPIView):
    """
        角色列表
    """
    permission_view = "view_role"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = StandardResultsSetPagination
    serializer_class = RoleSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ["name"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Role.objects.all().order_by('-id')
        else:
            queryset = Role.objects.none()
        return queryset


class RoleViewCreate(generics.CreateAPIView):
    """ 添加角色 """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = RoleCreateSerialize

    def create(self, request, *args, **kwargs):
        if request.data.get("name") is not None:
            line = Role.objects.filter(name=request.data.get("name"))
            if len(line) != 0:
                return Response({"detail": "名称已存在！"})
            try:
                if request.data.get("permission") is not None:
                    role = Role()
                    role.name = request.data.get("name")
                    role.comment = request.data.get("comment")
                    role.save()

                    for p in request.data.get("permission"):
                        perm = Permission.objects.filter(id=int(p))
                        if perm:
                            role.permission.add(perm[0])
                else:
                    return Response({"detail": "角色不能为空！"})
            except Exception as e:
                logger.error("{0}".format(str(e)))
                return Response({"detail": "异常参数错误！"})
            return Response({"id": role.id})
        return Response({"detail": "名称不能为空！"})


class RoleViewUpdate(generics.CreateAPIView):
    """ 更新角色 """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = RoleCreateSerialize
    queryset = Role.objects.all()

    def update(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "pk不能None！"})
        try:
            if request.data.get("permission") is not None:
                line = Role.objects.filter(id=int(kwargs.get("pk")))
                if len(line) == 1:
                    for p in line.permission.all():
                        line.permission.remove(p)
                    for h in request.data.get("permission"):
                        lst = Permission.objects.filter(id=int(h))
                        if lst:
                            line.permission.add(lst[0])

                    Role.objects.filter(id=int(kwargs.get("pk"))).update(
                        name=request.data.get("name"),
                        comment=request.data.get("comment")
                    )
            else:
                return Response({"detail": "角色不能为空！"})
        except Exception as e:
            logger.error("{0}".format(str(e)))
            return Response({"detail": "异常参数错误！"})
        return Response({"id": kwargs.get("pk")})


class RoleViewDelete(generics.DestroyAPIView):
    """ 删除角色 """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = RoleCreateSerialize
    queryset = Role.objects.all()

    def delete(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "pk不能None！"})

        Role.objects.filter(id=int(kwargs.get("pk"))).delete()
        return Response({"id": kwargs.get("pk")})
