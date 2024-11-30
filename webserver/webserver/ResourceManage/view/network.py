#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.ResourceManage.models import Network
from .serializers import NetworkSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from webserver.common.permissions import IsOrgAdmin


class NetworkViewList(generics.ListAPIView):
    """
        网络设备列表
    """
    permission_view = "view_network"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = NetworkSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "address", "status"]
    search_fields = ["name"]

    def get_queryset(self):
        queryset = Network.objects.all().order_by('-create_time')
        return queryset
