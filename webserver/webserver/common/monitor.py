#!/usr/bin/env python
# -*- coding:utf-8 -*-

from webserver.settings import WORKDIR
from yaml import load, dump, Loader
from webserver.common import api
from webserver.defaultConfig.monitor_config import monitor_default_config


class Cfg(object):
    filename = "{0}/webserver/config/monitor.yml".format(WORKDIR)

    def is_exist(self):
        return True if api.Api.path_exists(self.filename) else False

    @classmethod
    def read_all(cls):
        if cls().is_exist() is False:
            return None
        with open(cls.filename, "r") as f:
            response_data = load(f, Loader=Loader)
        return response_data

    @classmethod
    def get(cls, name):
        with open(cls.filename, "r") as f:
            response_data = load(f, Loader=Loader)
        return response_data.get(name)

    @classmethod
    def write(cls, response_data):
        with open(cls.filename, "w") as f:
            dump(response_data, f)

    @classmethod
    def write_default(cls):
        with open(cls.filename, "w") as f:
            dump(monitor_default_config, f)
