#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.ResourceManage.models import Certificate
from .serializers import CertificateSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from webserver.common.permissions import IsOrgAdmin


class CertificateViewList(generics.ListAPIView):
    """
        主机凭证列表
    """
    permission_view = "view_certificate"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = CertificateSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "ssh_user"]
    search_fields = ["name"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Certificate.objects.all().order_by('-create_time')
        else:
            queryset = Certificate.objects.none()
        return queryset
