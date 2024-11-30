#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.AuditManage.models import Login, Option, CommandRecord, ConnectRecord
from .serializers import LoginSerializer, OptionSerializer, CommandSerializer, ConnectSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import filters

from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from webserver.common.permissions import IsOrgAdmin


class LoginViewList(generics.ListAPIView):
    """
        登录记录
    """
    permission_view = "view_audit_login"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = LoginSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ["username"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Login.objects.all().order_by('-id')
        else:
            queryset = Login.objects.filter(username=self.request.user.username).order_by('-id')
        return queryset


class OptionViewList(generics.ListAPIView):
    """
        操作记录
    """
    permission_view = "view_audit_option"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = OptionSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ["username"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Option.objects.all().order_by('-id')
        else:
            queryset = Option.objects.filter(username=self.request.user.username).order_by('-id')
        return queryset


class CommandViewList(generics.ListAPIView):
    """
        命令审计
    """
    permission_view = "view_audit_command"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = CommandSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ["username"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = CommandRecord.objects.filter(log_type="command").order_by('-id')
        else:
            queryset = CommandRecord.objects.filter(
                username=self.request.user.username,
                log_type="command"
            ).order_by('-id')
        return queryset


class ConnectViewList(generics.ListAPIView):
    """
        连接审计
    """
    permission_view = "view_audit_connect"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = ConnectSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = []

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = ConnectRecord.objects.all().order_by('-id')
        else:
            queryset = ConnectRecord.objects.filter(username_id=self.request.user.id).order_by('-id')
        return queryset
