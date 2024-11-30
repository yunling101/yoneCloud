#!/usr/bin/env python
# -*- coding:utf-8 -*-

import consul
from webserver.common import monitor


class CC(object):
    def __init__(self):
        self.connect = self.connect()

    @staticmethod
    def connect():
        cfg = monitor.Cfg.get("consul")
        if cfg.get("token") is not None and cfg["token"] != "":
            conn = consul.Consul(host=cfg["address"], port=cfg["port"], token=cfg["token"], scheme="http")
        else:
            conn = consul.Consul(host=cfg["address"], port=cfg["port"], scheme="http")
        return conn

    def register(self, name, service_id, address, port, hostname, business):
        self.connect.agent.service.register(
           name, service_id=service_id,
           address=address,
           port=port,
           meta={"hostname": hostname, "business": business},
           tags=["prod"]
        )

    def network(self, name, service_id, address):
        self.connect.agent.service.register(
            name, service_id=service_id,
            address=address,
            tags=["snmp"]
        )

    def deregister(self, service_id):
        self.connect.agent.service.deregister(service_id)
