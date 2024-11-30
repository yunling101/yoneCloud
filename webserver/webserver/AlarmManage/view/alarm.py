#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.AlarmManage.models import AlarmApplication, AlarmRoute, AlarmRule
from .serializers import AlarmSerializer, AlarmRouteSerializer, AlarmRuleSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from webserver.common.permissions import IsOrgAdmin
from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class AlarmRuleList(generics.ListAPIView):
    """
        规则列表
    """
    permission_view = "view_alarm_rule"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = AlarmRuleSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ["name", "alarm_group"]

    def get_queryset(self):
        queryset = AlarmRule.objects.all().order_by("-id")
        return queryset


class AlarmApplicationList(generics.ListAPIView):
    """
        应用监控列表
    """
    permission_view = "view_alarm_application"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = AlarmSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ["sid", "name"]

    def get_queryset(self):
        queryset = AlarmApplication.objects.all().order_by("-id")
        return queryset


class AlarmRouteList(generics.ListAPIView):
    """
        报警路由列表
    """
    permission_view = "modify_alarm_config"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = AlarmRouteSerializer

    def get_queryset(self):
        queryset = AlarmRoute.objects.all().order_by("-id")
        return queryset
