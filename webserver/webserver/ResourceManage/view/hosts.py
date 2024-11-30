#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from webserver.ResourceManage.models import Hosts
from .serializers import HostsSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django.db.models import Q
from webserver.common.permissions import IsOrgAdmin
from rest_framework import generics
from webserver.common.api import ResultsLimitPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from webserver.AuthManage.models import Authorize
from webserver.common.api import Api


class HostsViewList(generics.ListAPIView):
    """
        主机池列表
    """
    permission_view = "view_hosts"
    operation_record = False

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsOrgAdmin,)
    pagination_class = ResultsLimitPagination
    serializer_class = HostsSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ["sid", "hostname", "ip", "instance_id"]
    search_fields = ["sid", "hostname", "ip", "instance_id"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Hosts.objects.filter(resource_pool=True).order_by('-create_time')
        else:
            # 多ID查询
            # Hosts.objects.filter(id__in=[1,2])
            queryset = Hosts.objects.none()
            auth = Authorize.objects.filter(user=self.request.user.id)
            if len(auth) == 1:
                for b in auth[0].business.all():
                    queryset |= Hosts.objects.filter(Q(business=b.id) & Q(resource_pool=True))
                for h in auth[0].hosts.all():
                    # 合并集合
                    # queryset.union(h)
                    queryset |= Hosts.objects.filter(Q(id=h.id) & Q(resource_pool=True))
        return self.query_filter_set(queryset)

    def filter_business(self, queryset):
        business = self.request.query_params.get("business")
        if not business:
            return queryset

        return queryset.filter(business__name=business)

    def filter_cloud(self, queryset):
        cloud = self.request.query_params.get("cloud")
        if not cloud:
            return queryset

        return queryset.filter(cloud=cloud)

    def filter_monitor(self, queryset):
        monitor = self.request.query_params.get("monitor")
        if not monitor:
            return queryset

        if monitor == "开启" or monitor == 1 or monitor == "1":
            return queryset.filter(monitor=1)
        return queryset.filter(monitor=0)

    def filter_status(self, queryset):
        status = self.request.query_params.get("status")
        if not status:
            return queryset

        if status == "正常" or status == "success":
            status = "success"
        elif status == "异常" or status == "failed":
            status = "failed"
        else:
            status = "unknown"
        return queryset.filter(status__contains=status)

    def filter_time(self, queryset):
        time = self.request.query_params.get("create_time")
        if not time:
            return queryset

        time = time.split(" - ")
        if len(time) == 2:
            start_date = Api.str_to_date(time[0])
            end_date = Api.str_to_date(time[1])
            return queryset.filter(create_time__range=(start_date, end_date))
        return queryset

    def query_filter_set(self, queryset):
        queryset = self.filter_business(queryset)
        queryset = self.filter_cloud(queryset)
        queryset = self.filter_monitor(queryset)
        queryset = self.filter_status(queryset)
        queryset = self.filter_time(queryset)
        queryset = queryset.distinct()
        return queryset
