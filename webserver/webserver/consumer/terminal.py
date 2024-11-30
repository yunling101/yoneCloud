#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import select
import time
import json
import re
import socket
import codecs
import os

from webserver.common import api
# from paramiko.py3compat import u
from webserver.AuditManage.models import CommandRecord, ConnectRecord
from .commandextract import CommandDeal
from webserver.settings import MEDIA_ROOT
from django.utils import timezone


class InterActiveShellThread(threading.Thread):
    def __init__(self, channel, chan, log_name=None, width=90, height=40, username=None):
        super(InterActiveShellThread, self).__init__()
        self.channel = channel
        self.chan = chan
        self.log_name = log_name
        self.width = width
        self.height = height
        self.username = username

    def term_log(self, begin_time, stdout, log_name):
        attrs = {
            "version": 1,
            "width": 110,
            "height": 30,
            "duration": round(time.time() - begin_time, 6),
            "command": os.environ.get('SHELL', None),
            'title': None,
            "env": {
                "TERM": os.environ.get('TERM'),
                "SHELL": os.environ.get('SHELL', 'sh')
            },
            'stdout': list(map(lambda frame: [round(frame[0], 6), frame[1]], stdout))
        }
        api.Api.mkdir_p('/'.join(os.path.join(MEDIA_ROOT, log_name).rsplit('/')[0:-1]))
        with open(os.path.join(MEDIA_ROOT, log_name), "a") as f:
            f.write(json.dumps(attrs, ensure_ascii=True, cls=api.FloatEncoder, indent=2))

        audit_log = ConnectRecord.objects.get(
            channel=self.channel.channel_name,
            log=log_name.rsplit('/')[-1]
        )
        audit_log.is_finished = True
        audit_log.end_time = timezone.now()
        audit_log.save()

    def run(self):
        command, stdout = list(), list()
        begin_time = time.time()
        last_write_time = {'last_activity_time': begin_time}
        log = ConnectRecord.objects.get(channel=self.channel.channel_name)

        vim_flag = False
        vim_data = ''
        try:
            self.chan.settimeout(0.0)
            data = None
            while True:
                try:
                    r, w, x = select.select([self.chan], [], [])
                    if self.chan in r:
                        data = self.chan.recv(1024)
                        x = data
                        if isinstance(data, bytes):
                            x = data.decode("utf-8", "ignore")  # u(data)
                        if x == "closed":
                            self.chan.close()
                            api.logger.info("close ssh session")
                            break
                        if len(x) == 0:
                            break

                        now = time.time()
                        delay = now - last_write_time['last_activity_time']
                        last_write_time['last_activity_time'] = now

                        if x == "logout\r\n" or x == "logout":
                            self.chan.close()
                        else:
                            if vim_flag:
                                vim_data += x
                            if '\r\n' not in x:
                                command.append(x)
                            else:
                                command_result = CommandDeal().deal_command(''.join(command))
                                if len(command_result) != 0:
                                    if command_result.strip().startswith('vi') or command_result.strip().startswith('fg'):
                                        CommandRecord.objects.create(
                                            log_id=log.id,
                                            log_type="ssh",
                                            username=self.username,
                                            command=command_result[0:255]
                                        )
                                        vim_flag = True
                                    else:
                                        if vim_flag:
                                            if re.compile('\[.*@.*\][\$#]').search(vim_data):
                                                vim_flag = False
                                                vim_data = ''
                                        else:
                                            CommandRecord.objects.create(
                                                log_id=log.id,
                                                log_type="ssh",
                                                username=self.username,
                                                command=command_result[0:255]
                                            )
                                command = list()

                            if isinstance(x, str):
                                stdout.append([delay, x])
                            else:
                                stdout.append([delay, codecs.getincrementaldecoder("UTF-8")("replace").decode(x)])

                        if isinstance(data, bytes):
                            data = data.decode("utf-8", "ignore")
                        self.channel.send(data)

                except socket.timeout:
                    break
                except Exception as e:
                    api.logger.error("Exception InterActiveShellThread error: {0}".format(str(e)))
                    self.channel.send(data)
        finally:
            self.chan.transport.close()
            self.channel.close()
            self.term_log(begin_time, stdout, self.log_name)
