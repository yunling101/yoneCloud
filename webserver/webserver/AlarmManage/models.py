#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from webserver.website.models import TablePrefix


class AlarmRoute(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="名称")
    # group_by 路由配置后会匹配告警label和value相同才能生到同组内
    group_by = models.CharField(max_length=128, default="alertname", null=False, verbose_name="报警分组")
    # group_wait 分组收到告警后会等待group wait配置的时间，再发出报警，这样目地是同组在配置时间只发出一封报警邮件
    group_wait = models.CharField(max_length=16, default="30s", null=False, verbose_name="组报警等待时间")
    # 已有的Group等待group_interval指定的时间，判断Alert是否解决，当上次发送通知到现在的间隔大于repeat_interval或者Group有更新时会发送通知
    group_interval = models.CharField(max_length=16, default="300s", null=False, verbose_name="组报警间隔时间")
    # 当上次报警发出后，再收到告警信息发出报警时间周期
    repeat_interval = models.CharField(max_length=16, default="4h", null=False, verbose_name="重复报警间隔时间")
    # 匹配标签
    match = models.TextField(verbose_name="匹配标签")

    class Meta:
        db_table = TablePrefix + "_alarm_route"

    def __str__(self):
        return self.name


class AlarmRule(models.Model):
    name = models.CharField(max_length=32, verbose_name="名称")
    expression = models.CharField(max_length=255, verbose_name="表达式")
    interval = models.CharField(max_length=16, blank=True, null=False, verbose_name="间隔时间")
    alarm_group = models.CharField(max_length=32, verbose_name="分组")
    tags = models.CharField(max_length=64, verbose_name="标签")
    title = models.CharField(max_length=255, verbose_name="标题")
    content = models.CharField(max_length=255, verbose_name="内容")
    desc = models.CharField(max_length=128, verbose_name="描述")
    create_time = models.DateTimeField(auto_now=True, null=False, verbose_name="创建时间")

    class Meta:
        db_table = TablePrefix + "_alarm_rule"

    def __str__(self):
        return self.name


class AlarmTemplate(models.Model):
    cname = models.CharField(max_length=32, verbose_name="中文名称")
    ename = models.CharField(max_length=32, verbose_name="英文名称")
    config = models.TextField(verbose_name="配置")

    class Meta:
        db_table = TablePrefix + "_alarm_template"

    def __str__(self):
        return self.cname


class AlarmGlobalConfig(models.Model):
    cname = models.CharField(max_length=32, verbose_name="中文名称")
    ename = models.CharField(max_length=32, verbose_name="英文名称")
    config = models.TextField(verbose_name="配置")

    class Meta:
        db_table = TablePrefix + "_alarm_global_config"

    def __str__(self):
        return self.cname


class AlarmConfig(models.Model):
    cname = models.CharField(max_length=32, verbose_name="中文名称")
    ename = models.CharField(max_length=32, verbose_name="英文名称")
    route = models.ForeignKey(AlarmRoute, null=True, blank=True, on_delete=models.CASCADE, verbose_name="关联路由")
    config = models.TextField(verbose_name="配置")

    class Meta:
        db_table = TablePrefix + "_alarm_config"

    def __str__(self):
        return self.cname


class AlarmApplication(models.Model):
    sid = models.BigIntegerField(unique=True, null=False, verbose_name="序列ID")
    name = models.CharField(max_length=56, null=False, verbose_name="应用名称")
    address = models.CharField(max_length=255, null=False, verbose_name="应用地址")
    status = models.BooleanField(default=True, verbose_name="状态")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = TablePrefix + "_alarm_application"

    def __str__(self):
        return self.name
