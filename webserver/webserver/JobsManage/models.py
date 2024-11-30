#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from webserver.website.models import TablePrefix


class JobsTemplate(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="模板名称")
    content = models.TextField(verbose_name="模板内容")
    status = models.BooleanField(default=False, verbose_name="模板状态")
    comment = models.CharField(max_length=512, blank=True, null=True, verbose_name="备注信息")
    create_time = models.DateTimeField(auto_now=True, null=False, verbose_name="创建时间")

    class Meta:
        db_table = TablePrefix + "_jobs_template"

    def __str__(self):
        return self.name


class JobsNotify(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="名称")
    alias = models.CharField(max_length=64, verbose_name="别名")
    address = models.CharField(max_length=255, verbose_name="地址")
    content = models.TextField(verbose_name="内容")
    status = models.BooleanField(default=False, verbose_name="状态")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注信息")
    create_time = models.DateTimeField(auto_now=True, null=False, verbose_name="创建时间")

    class Meta:
        db_table = TablePrefix + "_jobs_notify"

    def __str__(self):
        return self.name
