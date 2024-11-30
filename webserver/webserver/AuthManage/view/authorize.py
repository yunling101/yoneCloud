#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.AuthManage.models import Authorize
from .serializers import AuthorizeSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from webserver.common.permissions import IsOrgAdmin


class AuthorizeViewList(generics.ListAPIView):
    """
        主机授权列表
    """
    permission_view = "view_authorize"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = AuthorizeSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ["name"]
    search_fields = ["name"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Authorize.objects.all().order_by('-create_time')
        else:
            queryset = Authorize.objects.none()
        return queryset
