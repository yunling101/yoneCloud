#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver.ResourceManage.models import Certificate
from rest_framework import serializers
from webserver.common.mixins import BulkSerializerMixin
from webserver.AuthManage.models import Authorize


class CertificateSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Certificate
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class AuthorizeSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.SerializerMethodField()
    business = serializers.SerializerMethodField()

    class Meta:
        model = Authorize
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"

    def get_user(self, obj):
        if len(obj.user.all()) == 1:
            return obj.user.get().username
        return ""

    def get_hosts(self, obj):
        return len(obj.hosts.all())

    def get_business(self, obj):
        return [b.name for b in obj.business.all()]
