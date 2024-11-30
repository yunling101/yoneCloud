#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver.SystemManage.models import Recycle
from rest_framework import serializers
from webserver.common.mixins import BulkSerializerMixin


class RecycleSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Recycle
        list_serializer_class = serializers.ListSerializer
        exclude = ("data",)
