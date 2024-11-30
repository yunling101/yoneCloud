#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import datetime
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.BusinessManage.models import Business


def main():
    name = "默认业务"
    if Business.objects.filter(name=name).exists() is False:
        business, created = Business.objects.get_or_create(
            name=name,
            life_cycle="",
            maintainer="",
            tester="",
            create_time=datetime.datetime.now(),
        )
        if created:
            print("Business insert success: {0}".format(business.id))
    else:
        print("Business insert already exists")


if __name__ == "__main__":
    main()
