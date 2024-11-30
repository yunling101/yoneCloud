#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.website.models import Rule
from .serializers import RuleSerializer, RuleCreateSerialize
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from rest_framework import generics
from webserver.common.permissions import IsOrgAdmin
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from webserver.common.api import logger
from django.views.generic import View


class RuleViewList(generics.GenericAPIView):
    """
        菜单规则列表
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    serializer_class = RuleSerializer
    # permission_classes = (IsOrgAdmin,)
    queryset = Rule.objects.all().order_by('-id')

    # filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    # search_fields = ["title", "name"]

    # def get_queryset(self):
    #     queryset = Rule.objects.all().order_by('-id')
    #     return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_serializer())
        return Response(serializer.data)


class RuleViewCreate(generics.CreateAPIView):
    """
        添加菜单规则
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = RuleCreateSerialize

    def create(self, request, *args, **kwargs):
        if request.data.get("name") is not None:
            line = Rule.objects.filter(name=request.data.get("name"))
            if len(line) != 0:
                return Response({"detail": "名称已存在！"})
            try:
                if request.data.get("title") is not None:
                    rule = Rule()
                    rule.name = request.data.get("name")
                    rule.title = request.data.get("title") if request.data.get("pid") == "0" else "&nbsp;├ " + request.data.get("title")
                    rule.icon = request.data.get("icon")
                    rule.comment = request.data.get("remark")
                    rule.ismenu = True if request.data.get("ismenu") == "1" else False
                    rule.condition = request.data.get("condition")
                    rule.weigh = int(request.data.get("weigh"))
                    rule.pid = int(request.data.get("pid"))
                    rule.haschild = True if request.data.get("pid") == "0" else False
                    rule.status = True if int(request.data.get("status")) == 1 else False
                    rule.spacer = "&nbsp;├" if request.data.get("pid") != "0" else ""
                    rule.save()
                else:
                    return Response({"detail": "标题不能为空！"})
            except Exception as e:
                logger.error("{0}".format(str(e)))
                return Response({"detail": "异常参数错误！"})
            return Response({"id": rule.id})
        return Response({"detail": "名称不能为空！"})


class RuleViewUpdate(generics.CreateAPIView):
    """
        更新菜单规则
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = RuleCreateSerialize
    queryset = Rule.objects.all()

    def update(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "pk不能None！"})
        try:
            if request.data.get("name") is not None:
                line = Rule.objects.filter(id=int(kwargs.get("pk")))
                if len(line) == 1:
                    Rule.objects.filter(id=int(kwargs.get("pk"))).update(
                        name=request.data.get("name"),
                        title=request.data.get("title") if request.data.get("pid") == "0" else "&nbsp;├ " + request.data.get("title"),
                        icon=request.data.get("icon"),
                        comment=request.data.get("remark"),
                        ismenu=True if request.data.get("ismenu") == "1" else False,
                        condition=request.data.get("condition"),
                        weigh=int(request.data.get("weigh")),
                        pid=int(request.data.get("pid")),
                        haschild=True if request.data.get("pid") == "0" else False,
                        status=True if int(request.data.get("status")) == 1 else False,
                        spacer="&nbsp;├" if request.data.get("pid") != "0" else ""
                    )
            else:
                return Response({"detail": "名称不能为空！"})
        except Exception as e:
            logger.error("{0}".format(str(e)))
            return Response({"detail": "异常参数错误！"})
        return Response({"id": kwargs.get("pk")})


class RuleViewDelete(generics.DestroyAPIView):
    """
        删除菜单规则
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    serializer_class = RuleCreateSerialize
    queryset = Rule.objects.all()

    def delete(self, request, *args, **kwargs):
        if kwargs.get("pk") is None:
            return Response({"detail": "pk不能None！"})

        Rule.objects.filter(id=int(kwargs.get("pk"))).delete()
        return Response({"id": kwargs.get("pk")})
