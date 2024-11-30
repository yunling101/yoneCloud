#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from uuid import uuid1
from webserver.ResourceManage.models import Hosts
from webserver.UserManage.models import User
from webserver.website.models import TablePrefix


class Login(models.Model):
    username = models.CharField(max_length=128, verbose_name="用户名")
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP地址")
    source = models.CharField(max_length=12, verbose_name="来源")
    hostname = models.CharField(max_length=128, null=True, verbose_name="来源主机名")
    session_key = models.CharField(max_length=40)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    attribution = models.CharField(max_length=40)
    logout_added = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = TablePrefix + "_audit_login"

    def __unicode__(self):
        return self.ip


class Option(models.Model):
    object = models.CharField(max_length=128, verbose_name="操作对象")
    ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP地址")
    date_added = models.DateTimeField(auto_now=True, null=True)
    attribution = models.CharField(max_length=40)
    username = models.CharField(max_length=128, verbose_name="用户名")

    class Meta:
        db_table = TablePrefix + "_audit_option"

    def __unicode__(self):
        return self.ip


class ConnectRecord(models.Model):
    server = models.ForeignKey(Hosts, on_delete=models.CASCADE, verbose_name="连接主机")
    channel = models.CharField(max_length=128, unique=True, verbose_name="连接通道")
    log = models.UUIDField(max_length=128, unique=True, default=uuid1, verbose_name="log")
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="连接用户")
    width = models.PositiveIntegerField(default=90, verbose_name="连接宽度")
    height = models.PositiveIntegerField(default=40, verbose_name="连接高度")
    is_finished = models.BooleanField(default=False, verbose_name="连接状态")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="开始时间")
    end_time = models.DateTimeField(auto_now_add=False, null=True, verbose_name="开始时间")

    class Meta:
        ordering = ['-start_time']
        db_table = TablePrefix + "_audit_connect"

    def __str__(self):
        return "{0}".format(self.log)


class CommandRecord(models.Model):
    log_id = models.IntegerField(null=True, verbose_name="唯一ID")
    log_type = models.CharField(max_length=64, verbose_name="类型")
    username = models.CharField(max_length=64, null=True, verbose_name="类型")
    command = models.TextField(verbose_name="命令")
    hosts = models.TextField(default="", verbose_name="主机")
    datetime = models.DateTimeField(auto_now=True, verbose_name="时间")

    class Meta:
        ordering = ['-datetime']
        db_table = TablePrefix + "_audit_command"

    def __int__(self):
        return self.log_id
