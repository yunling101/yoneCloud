#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .api import ajax_http, validate_logon
from django.views.generic import View
from django.utils.decorators import method_decorator


class LoginValidate(object):
    @method_decorator(validate_logon)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginValidate, self).dispatch(request, *args, **kwargs)


class BaseView(View):
    @method_decorator(ajax_http)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseView, self).dispatch(request, *args, **kwargs)


@ajax_http
def http404(request):
    info = {"code": False, "msg": "啊哈，访问的页面不存在啦！"}
    return info


@ajax_http
def http500(request):
    info = {"code": False, "msg": "服务器无法响应您的请求，请联系管理员！"}
    return info
