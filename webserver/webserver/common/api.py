#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import IP
import logging
import random
import time
import datetime
import requests
import os
import crypt
import errno
import base64

from random import choice
from django.http import HttpResponse, HttpResponseRedirect
from webserver.AuditManage.models import Option
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict
from uuid import uuid1

logger = logging.getLogger("app.views")


class Api(object):
    @classmethod
    def json_load(cls, msg):
        data = json.loads(msg)
        return data

    @classmethod
    def json_dump(cls, msg, ensure_ascii=False):
        data = json.dumps(msg, ensure_ascii=ensure_ascii)
        return data

    @classmethod
    def path_exists(cls, path):
        return True if os.path.exists(path) else False

    @classmethod
    def get_sid(cls, num):
        rest = str(random.randint(0000000000000000, 9999999999999999))[:num]
        return rest

    @classmethod
    def sftime(cls, formatting=None):
        if formatting is not None:
            return "{0}".format(time.strftime(formatting, time.localtime(time.time())))
        return"{0}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

    @classmethod
    def number_day(cls, num):
        now = datetime.datetime.now()
        return now + datetime.timedelta(days=num)

    @classmethod
    def start_time(cls, current):
        return datetime.datetime.combine(current.date(), datetime.time.min)

    @classmethod
    def end_time(cls, current):
        return datetime.datetime.combine(current.date(), datetime.time.max)

    @classmethod
    def str_to_date(cls, string):
        return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S").date()

    @classmethod
    def rand(cls, number):
        """
            生成随机码
        """
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        salt_list = []
        for i in range(number):
            salt_list.append(choice(seed))
        salt = ''.join(salt_list)
        return salt

    @classmethod
    def mkdir_p(cls, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise

    @classmethod
    def crypt_sha512(cls, word, salt):
        return crypt.crypt(word, salt)

    @classmethod
    def uuid(cls):
        return uuid1()

    @classmethod
    def base64(cls, msg: bytes) -> str:
        return base64.b64encode(msg).decode()


def ajax_http(func):
    def wrp(request, *args, **kwargs):
        if request.method == "GET":
            callback = request.GET.get('callback')
        elif request.method == "POST":
            callback = request.GET.get('callback')
        else:
            callback = None

        info = func(request)
        info = Api.json_dump(info)

        if callback is None:
            info = info
        else:
            info = "{0}({1})".format(callback, info)
        response = HttpResponse(info, content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET"
        response["Access-Control-Allow-Credentials"] = True
        response["Access-Control-Allow-Headers"] = "Cache-Control"
        return response
    return wrp


def option_in_record(req, ctx, page):
    info = {"content": "", "status": False}
    if 'HTTP_X_FORWARDED_FOR' in req.META:
        client_ip = req.META['HTTP_X_FORWARDED_FOR']
    else:
        client_ip = req.META['REMOTE_ADDR']
    content = ctx.get("records", "")
    try:
        lst = Option()
        lst.ip = client_ip
        if content:
            lst.object = "【WEB】{0} 记录【{1}】".format(page,content)
        else:
            lst.object = "【WEB】{0}".format(page)
        lst.attribution = IP.find(client_ip)
        lst.username = req.user.username
        lst.save()
        info["status"] = True
    except Exception as e:
        info["content"] = str(e)
    return info


def validate_logon(func):
    def wrp(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/login/")
    return wrp


class StandardResultsSetPagination(PageNumberPagination):
    """
        配置分页规则
    """
    page_size = 10
    page__size_query_param = 'page_size'
    page_query_param = 'page'


class ResultsLimitPagination(LimitOffsetPagination):
    """
        Limit分页方式
    """
    max_limit = 100

    def get_paginated_response(self, data):
        code, msg = True, ""

        return Response(OrderedDict([
            ("code", code),
            ("msg", msg),
            ("total", self.count),
            ("rows", data)
        ]))


class FloatEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, float):
            return format(obj, '.6f')
        return json.JSONEncoder.encode(self, obj)

