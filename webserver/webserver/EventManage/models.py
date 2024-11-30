#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from webserver.website.models import TablePrefix


class Event(models.Model):
    event_id = models.CharField(max_length=128, null=True, verbose_name="事件ID")
    event_type = models.CharField(max_length=64, verbose_name="事件类型")
    event_title = models.CharField(max_length=512, verbose_name="事件标题")
    event_content = models.CharField(max_length=512, verbose_name="事件内容")
    username = models.CharField(max_length=64, verbose_name="接收用户")
    status = models.BooleanField(default=False, verbose_name="事件状态")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    class Meta:
        db_table = TablePrefix + "_event"

    def __str__(self):
        return str(self.event_title)
