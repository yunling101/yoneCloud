#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.AuditManage.models import Login, Option
from webserver.common.api import logger
from IP import find


class Record(object):
    """
        操作记录
    """
    @classmethod
    def login_records(cls, request, username, source, hostname):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            client_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            client_ip = request.META['REMOTE_ADDR']
        try:
            login_record = Login()
            login_record.ip = client_ip
            login_record.source = source
            login_record.hostname = hostname
            login_record.session_key = request.session.session_key
            login_record.username = username
            login_record.attribution = find(client_ip)
            login_record.save()
        except Exception as e:
            logger.error("{0}".format(str(e)))

    @classmethod
    def operation_records(cls, request, view, content):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            client_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            client_ip = request.META['REMOTE_ADDR']
        try:
            operation_record = Option()
            operation_record.ip = client_ip
            if content:
                operation_record.object = "【WEB】{0} 记录【{1}】".format(view, content)
            else:
                operation_record.object = "【WEB】{0}".format(view)
            request.attribution = find(client_ip)
            operation_record.username = request.user.username
            operation_record.save()
        except Exception as e:
            logger.error("{0}".format(str(e)))
