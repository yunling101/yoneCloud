#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver.TaskManage.models import TaskTimer, TaskTimerResults
from rest_framework import serializers
from webserver.common.mixins import BulkSerializerMixin


class TaskTimerSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = TaskTimer
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"

    def get_results(self, obj):
        results = TaskTimerResults.objects.filter(uuid=obj.uuid)
        return len(results)
