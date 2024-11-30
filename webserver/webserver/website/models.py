#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from webserver.settings import TablePrefix


class Rule(models.Model):
    name = models.CharField(max_length=56, unique=True, verbose_name="名称")
    title = models.CharField(max_length=56, verbose_name="标题")
    pid = models.IntegerField(blank=True, null=False, verbose_name="父节点")
    icon = models.CharField(max_length=32, verbose_name="图标")
    weigh = models.IntegerField(blank=True, null=False, verbose_name="权重")
    ismenu = models.BooleanField(default=True, verbose_name="是否菜单")
    spacer = models.CharField(max_length=32, verbose_name="间隔符")
    status = models.BooleanField(default=True, verbose_name="状态")
    condition = models.CharField(max_length=32, verbose_name="条件")
    haschild = models.BooleanField(default=True, verbose_name="是否有子菜单")
    priority = models.IntegerField(blank=True, null=False, default=0, verbose_name="优先级")
    create_time = models.DateTimeField(auto_now=True, null=False, verbose_name="创建时间")
    comment = models.CharField(max_length=256, blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return self.name

    class Meta:
        db_table = TablePrefix + "_auth_rule"
