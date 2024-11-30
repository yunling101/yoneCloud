#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.SystemManage.models import Recycle
from .serializers import RecycleSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from webserver.common.permissions import IsOrgAdmin


class RecycleViewList(generics.ListAPIView):
    """
        资源回收站
    """
    permission_view = "view_recycle"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = RecycleSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "ip"]
    search_fields = ["name", "ip", "type"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Recycle.objects.all().order_by('-id')
        else:
            queryset = Recycle.objects.none()
        return queryset
