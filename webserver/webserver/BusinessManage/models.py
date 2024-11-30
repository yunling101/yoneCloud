#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from webserver.website.models import TablePrefix


class Business(models.Model):
    name = models.CharField(max_length=56, unique=True, verbose_name="业务名称")
    life_cycle = models.CharField(max_length=32, verbose_name="生命周期")
    maintainer = models.CharField(max_length=32, verbose_name="运维人员")
    tester = models.CharField(max_length=32, verbose_name="测试人员")
    relevance = models.TextField(verbose_name="关联性")
    create_time = models.DateTimeField(auto_now=True, null=False, verbose_name='创建时间')

    class Meta:
        db_table = TablePrefix + "_business"

    def __str__(self):
        return self.name


class Cluster(models.Model):
    name = models.CharField(max_length=56, unique=True, verbose_name="名称")
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name="备注")

    class Meta:
        db_table = TablePrefix + "_cluster"

    def __str__(self):
        return self.name
