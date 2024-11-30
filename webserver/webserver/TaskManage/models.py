#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from webserver.ResourceManage.models import Hosts
from webserver.website.models import TablePrefix


class TaskTimer(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="名称")
    uuid = models.CharField(max_length=128, blank=False, unique=True, verbose_name="UUID")
    timer_type = models.CharField(max_length=32, verbose_name="定时类型")
    username = models.CharField(max_length=16, blank=True, null=False, verbose_name="创建用户")
    scripts = models.TextField(verbose_name="命令脚本")
    hosts = models.ManyToManyField(Hosts, verbose_name="主机")
    status = models.BooleanField(default=False, verbose_name="状态")
    notify = models.CharField(max_length=32, verbose_name="通知")
    retry_count = models.IntegerField(default=0, verbose_name="失败重试次数")
    description = models.TextField(verbose_name="描述")
    execution_time = models.CharField(max_length=128, verbose_name="执行时间")
    create_time = models.DateTimeField(auto_now=True, null=False, verbose_name="创建时间")

    class Meta:
        db_table = TablePrefix + "_task_timer"

    def __str__(self):
        return self.name


class TaskTimerResults(models.Model):
    uuid = models.CharField(max_length=128, null=False, verbose_name="UUID")
    frequency = models.IntegerField(blank=True, null=False, default=0, verbose_name="次数")
    status = models.CharField(max_length=128, null=True, verbose_name="状态")
    hosts = models.TextField(verbose_name="执行主机", null=True)
    results = models.TextField(verbose_name="执行输出")
    start_time = models.DateTimeField(null=True, verbose_name="开始时间")
    end_time = models.DateTimeField(null=True, verbose_name="结束时间")

    class Meta:
        db_table = TablePrefix + "_task_timer_results"

    def __str__(self):
        return self.uuid
