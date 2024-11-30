#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver.BusinessManage.models import Business
from rest_framework import serializers
from webserver.common.mixins import BulkSerializerMixin


class BusinessSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Business
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class BusinessCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ("name", "life_cycle", "maintainer", "tester", "relevance")
