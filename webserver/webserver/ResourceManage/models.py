#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from webserver.BusinessManage.models import Business
from webserver.website.models import TablePrefix
from django.utils import timezone


class Role(models.Model):
    name = models.CharField(max_length=56, unique=True, verbose_name="角色名称")
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name="备注")

    class Meta:
        db_table = TablePrefix + "_role"

    def __str__(self):
        return self.name


class Certificate(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="凭证名称")
    ssh_type = models.CharField(max_length=16, blank=True, null=False, verbose_name="类型")
    ssh_port = models.IntegerField(blank=True, null=False, verbose_name="端口")
    ssh_user = models.CharField(max_length=16, blank=True, null=False, verbose_name="用户")
    ssh_password = models.CharField(max_length=64, blank=True, null=True, verbose_name="密码")
    ssh_key = models.TextField(null=True, verbose_name="KEY内容")
    create_time = models.DateTimeField(auto_now=True, null=False, verbose_name='创建时间')

    class Meta:
        db_table = TablePrefix + "_certificate"

    def __str__(self):
        return self.name


class Hosts(models.Model):
    sid = models.BigIntegerField(unique=True, null=False, verbose_name="资源ID")
    instance_id = models.CharField(max_length=64, null=True, verbose_name="实例ID")
    instance_name = models.CharField(max_length=64, null=True, verbose_name="实例名称")
    instance_status = models.CharField(max_length=16, null=True, verbose_name="实例状态")
    alias = models.CharField(max_length=64, null=True, verbose_name="主机别名")
    hostname = models.CharField(max_length=128, null=False, verbose_name="主机名称")
    ip = models.GenericIPAddressField(verbose_name="公网IP")
    domain = models.CharField(max_length=255, blank=True, null=True, verbose_name="绑定域名")
    intranet = models.CharField(max_length=255, blank=True, null=True, verbose_name="内网IP, 多个逗号隔开")
    uuid = models.CharField(max_length=128, null=True, unique=True, verbose_name="主机全局唯一ID")
    certificate = models.ManyToManyField(Certificate, verbose_name="主机凭证")
    business = models.ManyToManyField(Business, verbose_name="业务绑定")
    relevance = models.CharField(max_length=16, null=True, verbose_name="关联性")
    monitor = models.BooleanField(default=False, verbose_name="监控状态")
    report = models.CharField(max_length=16, null=False, verbose_name="监控上报方式")
    role = models.ManyToManyField(Role, verbose_name="主机角色")
    cpu = models.CharField(max_length=64, blank=True, null=True, verbose_name="CPU核心")
    memory = models.CharField(max_length=64, blank=True, null=True, verbose_name="内存大小")
    disk = models.CharField(max_length=128, blank=True, null=True, verbose_name="磁盘大小")
    osname = models.CharField(max_length=64, blank=True, null=True, verbose_name="系统版本")
    proxy = models.BooleanField(default=False, verbose_name="是否开启代理")
    status = models.CharField(max_length=255, verbose_name="运行状态")
    provider = models.CharField(max_length=36, null=True, verbose_name="提供商")
    account = models.CharField(max_length=64, null=True, verbose_name="账户名")
    region = models.CharField(max_length=64, null=True, verbose_name="区域位置")
    resource_pool = models.BooleanField(default=True, verbose_name="是否放进资源池")
    security_group = models.CharField(max_length=128, null=True, verbose_name="安全组")
    agent_version = models.CharField(max_length=32, blank=True, null=True, verbose_name="Agent版本")
    model_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="资产型号")
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="序列号")
    asset_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="资产编号")
    comment = models.CharField(max_length=512, blank=True, null=True, verbose_name="备注信息")
    create_time = models.DateTimeField(auto_now=True, null=False, verbose_name="创建时间")
    update_time = models.DateTimeField(default=timezone.now, verbose_name="更新时间")
    deadline_time = models.CharField(max_length=128, null=True, verbose_name="到期时间")

    class Meta:
        db_table = TablePrefix + "_hosts"

    def __str__(self):
        return self.ip


class Group(models.Model):
    name = models.CharField(max_length=56, unique=True, verbose_name="分组名称")
    hosts = models.ManyToManyField(Hosts, verbose_name="主机")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = TablePrefix + "_group"

    def __str__(self):
        return self.name


class Network(models.Model):
    name = models.CharField(max_length=128, verbose_name="设备名称")
    address = models.CharField(max_length=256, verbose_name="地址")
    monitoring_status = models.BooleanField(default=False, verbose_name="监控状态")
    network_type = models.CharField(max_length=32, verbose_name="设备类型")
    network_model = models.CharField(max_length=128, verbose_name="设备型号")
    equipment = models.CharField(max_length=128, verbose_name="设备编号")
    region = models.CharField(max_length=128, null=True, verbose_name="设备位置")
    status = models.CharField(max_length=32, verbose_name="设备状态")
    other_info = models.TextField(verbose_name="其他信息")
    create_time = models.DateTimeField(auto_now=True, null=True, verbose_name="创建时间")

    class Meta:
        db_table = TablePrefix + "_network"

    def __str__(self):
        return self.name
