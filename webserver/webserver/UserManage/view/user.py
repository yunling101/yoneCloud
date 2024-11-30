#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.UserManage.models import User
from .serializers import UserSerializer, UserCreateSerialize, UserChangePasswordSerialize
from webserver.common.permissions import IsOrgAdmin
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response

from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from webserver.common.permissions import PermissionViewMixin
from webserver.common.api import Api, logger


class UserViewList(generics.ListAPIView):
    """
        用户列表
    """
    permission_view = "view_user"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ["id", "sid", "username", "role"]
    search_fields = ["username", "nickname", "email"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = User.objects.all().order_by('-id')
        else:
            queryset = User.objects.filter(username=self.request.user.username).order_by('-id')
        return queryset


class UserViewCreate(generics.CreateAPIView):
    """
        添加用户
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = UserCreateSerialize

    def create(self, request, *args, **kwargs):
        if request.data.get("sid") is None:
            request.data["sid"] = Api.get_sid(6)
        line = User.objects.filter(username=request.data.get("username"))
        if len(line) != 0:
            return Response({"detail": "用户已存在！"})
        user = User.objects.create_user(**request.data)
        return Response({"id": user.id})


class UserViewUpdate(PermissionViewMixin, generics.UpdateAPIView):
    """ 更新用户 """
    permission_view = "change_user"
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    serializer_class = UserCreateSerialize

    # 不添加此行会报，is not compatible with schema generation
    queryset = User.objects.all()

    # def get_queryset(self):
    #     queryset = User.objects.all()
    #     return queryset

    def update(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "pk不能None！"})
        try:
            User.objects.filter(id=int(kwargs.get("pk"))).update(
                email=request.data.get("email"),
                username=request.data.get("username"),
                nickname=request.data.get("nickname"),
                is_active=request.data.get("is_active"),
                is_superuser=request.data.get("is_superuser"),
                role_id=request.data.get("role_id")
            )
        except Exception as e:
            logger.error("{0}".format(str(e)))
            return Response({"detail": "异常参数错误！"})
        return Response({"id": kwargs.get("pk")})


class UserViewDelete(generics.DestroyAPIView):
    """ 删除用户 """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = UserCreateSerialize
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "pk不能None！"})

        User.objects.filter(id=int(kwargs.get("pk"))).delete()
        return Response({"id": kwargs.get("pk")})


class UserViewChangePassword(generics.UpdateAPIView):
    """
        修改密码
    """
    permission_view = "change_password"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    serializer_class = UserChangePasswordSerialize

    def get_queryset(self):
        if not self.request:
            return User.objects.none()
        return User.objects.all()
        
    def update(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "id不能为空！"})
        try:
            if request.user.check_password(request.data.get("old_password")):
                if request.data.get("new_password") is None:
                    return Response({"detail": "new_password字段不能为空！"})

                user = User.objects.get(id=int(kwargs.get("pk")))
                user.set_password(request.data.get("new_password"))
                user.save()
            else:
                return Response({"detail": "old_password原密码验证错误！"})
        except Exception as e:
            logger.error("{0}".format(str(e)))
            return Response({"detail": "异常错误！"})

        return Response({"id": kwargs.get("pk")})
