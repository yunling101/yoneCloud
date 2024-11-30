#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver.website.models import Rule
from rest_framework import serializers
from webserver.common.mixins import BulkSerializerMixin


class RuleSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Rule
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class RuleCreateSerialize(serializers.ModelSerializer):
    model = Rule
    fields = ("name", "title", "pid", "icon", "weigh", "ismenu",
              "spacer", "status", "condition", "haschild", "comment"
              )
