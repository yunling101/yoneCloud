#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver.AuditManage.models import Login, Option, CommandRecord, ConnectRecord
from rest_framework import serializers
from webserver.common.mixins import BulkSerializerMixin
from webserver.UserManage.models import User
from webserver.ResourceManage.models import Hosts


class LoginSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Login
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class OptionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Option
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class CommandSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = CommandRecord
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class ConnectSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    server = serializers.SerializerMethodField()
    hostname = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = ConnectRecord
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"

    def get_server(self, obj):
        try:
            hosts = Hosts.objects.get(id=obj.server_id)
            return hosts.ip
        except:
            pass
        return ""

    def get_hostname(self, obj):
        try:
            hosts = Hosts.objects.get(id=obj.server_id)
            return hosts.hostname
        except:
            pass
        return ""

    def get_username(self, obj):
        try:
            user = User.objects.get(id=obj.username_id)
            return user.username
        except:
            pass
        return ""
