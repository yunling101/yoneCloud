#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver.ResourceManage.models import Hosts, Network, Group
from rest_framework import serializers
from webserver.common.mixins import BulkSerializerMixin
from webserver.common.api import Api
from webserver.common import monitor
from webserver.common.permissions import UserAuthorize


class HostsSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    ml = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    console = serializers.SerializerMethodField()

    class Meta:
        model = Hosts
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"

    def get_status(self, obj):
        try:
            info = Api.json_load(obj.status)
        except:
            info = {"time": Api.sftime(), "status": "failed"}
        return info

    def get_ml(self, obj):
        cfg = monitor.Cfg.get("grafana")
        address = "{0}/d/0000000002/zhu-ji-zi-yuan-jian-kong?orgId=1&var-hostname={1}".format(
            cfg["address"], obj.hostname)
        if self.context['request'].user.is_superuser:
            if obj.monitor:
                return address
        else:
            if obj.monitor:
                if UserAuthorize(uid=self.context['request'].user.id).get_monitor():
                    return address
        return False

    def get_console(self, obj):
        if self.context['request'].user.is_superuser:
            return True
        return UserAuthorize(uid=self.context['request'].user.id).get_console()


class GroupSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Group
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class NetworkSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    monitoring_address = serializers.SerializerMethodField()

    class Meta:
        model = Network
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"

    def get_monitoring_address(self, obj):
        cfg = monitor.Cfg.get("grafana")
        address = "{0}/d/0000000004/wang-luo-she-bei-jian-kong?orgId=1&var-instance={1}".format(
            cfg["address"], obj.address)
        if self.context['request'].user.is_superuser:
            if obj.monitoring_status:
                return address
        else:
            if obj.monitoring_status:
                if UserAuthorize(uid=self.context['request'].user.id).get_monitor():
                    return address
        return False
