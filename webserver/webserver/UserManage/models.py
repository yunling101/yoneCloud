#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from webserver.website.models import TablePrefix


class Permission(models.Model):
    name = models.CharField(max_length=64, null=False)
    menu = models.CharField(max_length=64, null=False)
    view = models.CharField(max_length=64, null=False)
    comment = models.CharField(max_length=128, null=True, verbose_name="备注")

    class Meta:
        db_table = TablePrefix + "_user_perm"

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=64)
    permission = models.ManyToManyField(Permission, blank=True)
    comment = models.CharField(max_length=128, null=True, verbose_name="备注")

    class Meta:
        db_table = TablePrefix + "_user_role"

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, sid, email, username, nickname, password=None, is_active=None, role=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            sid=sid,
            email=self.normalize_email(email),
            username=username,
            nickname=nickname,
            is_active=is_active,
            role_id=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, sid, email, username, nickname, password):
        if not email:
            raise ValueError("Users must have an email address")

        if self.model.objects.filter(sid=sid).exists() or self.model.objects.filter(username=username).exists():
            raise ValueError("A user with that email or username already exists")

        user = self.model(
            sid=sid,
            email=self.normalize_email(email),
            nickname=nickname,
            username=username
        )
        user.is_active = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user, True


class User(AbstractBaseUser):
    sid = models.BigIntegerField(unique=True, null=False, verbose_name="sid")
    username = models.CharField(max_length=40, unique=True, db_index=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    nickname = models.CharField(max_length=64, null=True)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.CASCADE)

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = TablePrefix + "_user"
        ordering = ['-id']

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

    @property
    def is_valid(self):
        if self.is_active:
            return True
        return False


class White(models.Model):
    ip = models.GenericIPAddressField(unique=True, verbose_name="IP地址")
    netmask = models.GenericIPAddressField(verbose_name="子网掩码")
    username = models.CharField(max_length=64, verbose_name="操作用户")
    create_time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=100)

    class Meta:
        db_table = TablePrefix + "_white"

    def __str__(self):
        return self.ip
