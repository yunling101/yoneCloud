#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.ResourceManage.models import Group
from .serializers import GroupSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from webserver.common.permissions import IsOrgAdmin


class GroupViewList(generics.ListAPIView):
    """
       分组列表
    """
    permission_view = "view_asset_group"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = GroupSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ["name"]

    def get_queryset(self):
        queryset = Group.objects.all().order_by("-id")
        return queryset
