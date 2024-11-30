#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.UserManage.models import User


def main():
    sid = 111111
    if User.objects.filter(sid=sid).exists() is False:
        user, created = User.objects.create_superuser(
            sid=sid,
            email="yunling101@gmail.com",
            nickname="超级管理员",
            username="yone",
            password="yone"
        )
        if created:
            print("User insert success: {0}".format(user.id))
    else:
        print("User insert already exists")


if __name__ == "__main__":
    main()
