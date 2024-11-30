#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.UserManage.models import Permission
from webserver.common.permissions import IsOrgAdmin
from .serializers import PermissionSerializer, PermissionCreateSerialize
from rest_framework.response import Response

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from webserver.common.api import ResultsLimitPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from webserver.common.api import logger


class PermissionViewList(generics.ListAPIView):
    """
        权限列表
    """
    permission_view = "view_permission"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = PermissionSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ["menu"]
    search_fields = ["name", "view"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Permission.objects.all().order_by('-id')
        else:
            queryset = Permission.objects.none()
        return queryset


class PermissionViewCreate(generics.CreateAPIView):
    """ 添加权限 """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = PermissionCreateSerialize

    def create(self, request, *args, **kwargs):
        if request.data.get("name") is not None:
            line = Permission.objects.filter(name=request.data.get("name"))
            if len(line) != 0:
                return Response({"detail": "名称已存在！"})
            try:
                permission = Permission()
                permission.name = request.data.get("name")
                permission.menu = request.data.get("menu")
                permission.view = request.data.get("view")
                permission.comment = request.data.get("comment")
                permission.save()
            except Exception as e:
                logger.error("{0}".format(str(e)))
                return Response({"detail": "异常参数错误！"})
            return Response({"id": permission.id})
        return Response({"detail": "名称不能为空！"})


class PermissionViewUpdate(generics.CreateAPIView):
    """ 更新权限 """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = PermissionCreateSerialize
    queryset = Permission.objects.all()

    def update(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "pk不能None！"})
        try:
            Permission.objects.filter(id=int(kwargs.get("pk"))).update(
                name=request.data.get("name"),
                menu=request.data.get("menu"),
                view=request.data.get("view"),
                comment=request.data.get("comment")
            )
        except Exception as e:
            logger.error("{0}".format(str(e)))
            return Response({"detail": "异常参数错误！"})
        return Response({"id": kwargs.get("pk")})


class PermissionViewDelete(generics.DestroyAPIView):
    """ 删除权限 """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = PermissionCreateSerialize
    queryset = Permission.objects.all()

    def delete(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "pk不能None！"})

        Permission.objects.filter(id=int(kwargs.get("pk"))).delete()
        return Response({"id": kwargs.get("pk")})
