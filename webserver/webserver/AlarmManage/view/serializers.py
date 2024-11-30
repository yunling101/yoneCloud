#!/usr/bin/env python
# -*- coding: utf-8 -*-


from webserver.AlarmManage.models import AlarmApplication, AlarmRoute, AlarmRule
from rest_framework import serializers
from webserver.common.mixins import BulkSerializerMixin


class AlarmRuleSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = AlarmRule
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class AlarmSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = AlarmApplication
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class AlarmRouteSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = AlarmRoute
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"
