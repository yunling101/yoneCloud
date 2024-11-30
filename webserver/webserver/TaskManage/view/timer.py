#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.TaskManage.models import TaskTimer
from .serializers import TaskTimerSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from webserver.common.permissions import IsOrgAdmin


class TaskTimerLists(generics.ListAPIView):
    """
        定时任务
    """
    permission_view = "view_task_timer"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = TaskTimerSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ["name"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = TaskTimer.objects.all().order_by('-id')
        else:
            queryset = TaskTimer.objects.filter(username=self.request.user.username)
        return queryset
