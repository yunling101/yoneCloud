#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channels.generic.websocket import WebsocketConsumer
from webserver.common.utils import WebSocketAuth
from webserver.common import api
from webserver.ResourceManage.models import Certificate, Hosts
from subprocess import Popen, PIPE
from webserver.settings import WORKDIR
from webserver.AuditManage.models import CommandRecord
from django.db.models import Q
from webserver.AuthManage.models import Authorize


class BatchCommand(WebsocketConsumer, WebSocketAuth):
    def connect(self):
        self.accept()
        if not self.scope["user"].is_authenticated:
            # self.send({"accept": True})
            self.send("session过期，请重新登录后再试！")
            self.close()

    def disconnect(self, code):
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
                data = api.Api.json_load(text_data)
                if isinstance(data, dict) and data["tp"] == "init":
                    data = data.get("data")
                    hosts = []
                    if self.scope["user"].is_superuser:
                        for b in data.get("business"):
                            h = Hosts.objects.filter(Q(business__name=b) | Q(business=None))
                            for i in h:
                                hosts.append(i.ip)
                    else:
                        auth = Authorize.objects.filter(user=self.scope["user"].id)
                        if len(auth) == 1:
                            for b in auth[0].business.all():
                                hosts = Hosts.objects.filter(business=b.id)
                                for h in hosts:
                                    hosts.append(h.ip)
                            for h in auth[0].hosts.all():
                                hosts.append(h.ip)

                    for x in data.get("hosts"):
                        h = Hosts.objects.filter(hostname=x)
                        if len(h) == 1:
                            if h[0].ip not in hosts:
                                hosts.append(h[0].ip)

                    cmd_bin = "{0}/bin/cmdChannel".format(WORKDIR)
                    cmd_bin += " --config {0}/webserver/config/default.ini batch".format(WORKDIR)
                    command = data.get("command").replace("\n", "\\n")
                    out = Popen('{0} --command "{1}" --hosts "{2}"'.format(cmd_bin, command, ','.join(hosts)),
                                shell=True,
                                stdout=PIPE
                                )
                    for seek in out.stdout.readlines():
                        self.send(seek.decode().strip("\n\n"))
                    try:
                        command_log = CommandRecord.objects.create(
                            log_id=api.Api.get_sid(6),
                            hosts=api.Api.json_dump(hosts),
                            username=self.scope["user"].username,
                            log_type="command",
                            command=command
                        )
                        command_log.save()
                    except Exception as e:
                        api.logger.error("{0}".format(str(e)))
                    self.close()
                elif isinstance(data, dict) and data["tp"] == "close":
                    self.disconnect(1)
                else:
                    self.send(text_data)
            elif bytes_data:
                self.send(bytes_data)
        except Exception as e:
            api.logger.error("{0}".format(str(e)))
            self.send("未知错误，请联系管理！")
            self.close()
