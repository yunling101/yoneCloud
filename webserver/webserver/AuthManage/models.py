#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from webserver.UserManage.models import User
from webserver.ResourceManage.models import Hosts
from webserver.BusinessManage.models import Business
from webserver.website.models import TablePrefix


class Authorize(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="授权名称")
    hosts = models.ManyToManyField(Hosts, verbose_name="主机授权")
    business = models.ManyToManyField(Business, verbose_name="业务授权")
    console = models.TextField(verbose_name="web console授权")
    user = models.ManyToManyField(User, verbose_name="授权用户")
    superuser = models.BooleanField(default=False, verbose_name="是否开启管理员")
    comment = models.TextField(verbose_name="备注信息")
    create_time = models.DateTimeField(auto_now=True, null=False, verbose_name="创建时间")

    class Meta:
        db_table = TablePrefix + "_authorize"

    def __str__(self):
        return self.name
