#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.JobsManage.models import JobsNotify
from .serializers import JobsNotifySerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from webserver.common.permissions import IsOrgAdmin


class JobsNotifyLists(generics.ListAPIView):
    """
        作业通知列表
    """
    permission_view = "view_jobs_notify"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = JobsNotifySerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ["name"]

    def get_queryset(self):
        queryset = JobsNotify.objects.all().order_by('-id')
        return queryset
