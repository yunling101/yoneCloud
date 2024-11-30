#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.BusinessManage.models import Business
from .serializers import BusinessSerializer, BusinessCreateSerialize
from webserver.common.permissions import IsOrgAdmin
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response

from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from webserver.common.api import Api, logger
from webserver.common.schema import Schema
from webserver.AuthManage.models import Authorize


class BusinessViewList(generics.ListAPIView):
    """
        业务列表
    """
    permission_view = "view_business"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = BusinessSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ["id"]
    search_fields = ["name"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Business.objects.all().order_by('-id')
        else:
            queryset = Business.objects.none()
            auth = Authorize.objects.filter(user=self.request.user.id)
            if len(auth) == 1:
                for b in auth[0].business.all():
                    queryset |= Business.objects.filter(id=b.id)
        return queryset


class BusinessViewCreate(generics.CreateAPIView):
    """
        添加业务
    """
    permission_view = "add_business"

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = BusinessCreateSerialize

    schema_parse = Schema(description="添加业务")
    schema_parse.push(name="name", required=True, description="业务名称")
    schema_parse.push(name="life_cycle", description="生命周期")
    schema_parse.push(name="maintainer", description="运维人员")
    schema_parse.push(name="tester", description="测试人员")
    schema = schema_parse.schema()

    def create(self, request, *args, **kwargs):
        if request.data.get("name") is not None:
            line = Business.objects.filter(name=request.data.get("name"))
            if len(line) != 0:
                return Response({"detail": "业务已存在！"})
            try:
                business = Business()
                business.name = request.data.get("name")
                business.life_cycle = "" if request.data.get("life_cycle") is None else request.data["life_cycle"]
                business.maintainer = "" if request.data.get("maintainer") is None else request.data.get("maintainer")
                business.tester = "" if request.data.get("tester") is None else request.data.get("tester")
                business.save()
                return Response({"id": business.id})
            except Exception as e:
                logger.error("{0}".format(str(e)))
                return Response({"detail": "未知异常错误！"})
        else:
            return Response({"detail": "参数错误！"})


class BusinessViewDelete(generics.DestroyAPIView):
    """
        删除业务
    """
    permission_view = "delete_business"

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = BusinessCreateSerialize
    queryset = Business.objects.all()

    def delete(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "id不能为空！"})

        Business.objects.filter(id=int(kwargs.get("pk"))).delete()
        return Response({"id": kwargs.get("pk")})


class BusinessViewUpdate(generics.UpdateAPIView):
    """
        更新业务
    """
    permission_view = "add_business"

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = BusinessCreateSerialize
    queryset = Business.objects.all()

    def update(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "id不能为空！"})
        try:
            if request.data.get("name") is None:
                return Response({"detail": "业务名称不能为空！"})

            Business.objects.filter(id=int(kwargs.get("pk"))).update(
                name=request.data.get("name"),
                life_cycle="" if request.data.get("life_cycle") is None else request.data["life_cycle"],
                maintainer="" if request.data.get("maintainer") is None else request.data.get("maintainer"),
                tester="" if request.data.get("tester") is None else request.data.get("tester")
            )
        except Exception as e:
            logger.error("{0}".format(str(e)))
            return Response({"detail": "未知异常错误！"})

        return Response({"id": kwargs.get("pk")})
