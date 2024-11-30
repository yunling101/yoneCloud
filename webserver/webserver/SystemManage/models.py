#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from webserver.website.models import TablePrefix


class Config(models.Model):
    cname = models.CharField(max_length=32, unique=True, verbose_name="中文名称")
    ename = models.CharField(max_length=32, unique=True, verbose_name="英文名称")
    config = models.TextField(verbose_name="配置")

    class Meta:
        db_table = TablePrefix + "_system_config"

    def __str__(self):
        return self.cname


class Recycle(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="名称")
    ip = models.GenericIPAddressField(unique=True, blank=False, verbose_name="IP地址")
    type = models.CharField(max_length=12, verbose_name="类型")
    data = models.TextField(verbose_name="数据")
    username = models.CharField(max_length=64, null=True, verbose_name="用户名")
    create_time = models.DateTimeField(auto_now=True, null=False, verbose_name='创建时间')

    class Meta:
        db_table = TablePrefix + "_recycle"

    def __str__(self):
        return self.name
