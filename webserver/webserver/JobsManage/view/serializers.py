#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver.JobsManage.models import JobsTemplate, JobsNotify
from rest_framework import serializers
from webserver.common.mixins import BulkSerializerMixin


class JobsTemplateSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = JobsTemplate
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class JobsNotifySerializer(BulkSerializerMixin, serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = JobsNotify
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"
