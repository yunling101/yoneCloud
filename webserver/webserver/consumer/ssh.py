#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paramiko
import socket
import os

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from webserver.common import api
from channels.generic.websocket import WebsocketConsumer
from webserver.common.utils import WebSocketAuth
from .terminal import InterActiveShellThread
from webserver.ResourceManage.models import Hosts, Certificate
from paramiko.ssh_exception import AuthenticationException
from webserver.AuditManage.models import CommandRecord, ConnectRecord
from webserver.UserManage.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now


class WebTerminal(WebsocketConsumer, WebSocketAuth):
    """
        1、建立WebSocket连接，并SSH连接到主机
        2、将 paramiko 返回的结果通过 websocket 返回给用户
        3、用户输入数据通过channel发送到服务器，执行后返回到WebSocket
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ssh = paramiko.SSHClient()
        self.chan = None

    def connect(self):
        self.accept()
        if not self.scope["user"].is_authenticated:
            self.send("session过期，请重新登录后再试！")
            self.close()

    def disconnect(self, code):
        try:
            self.chan.transport.close()
            self.chan.close()
            self.ssh.close()

            audit_log = ConnectRecord.objects.get(
                username=User.objects.get(username=self.scope["user"].username),
                channel=self.channel_name
            )
            audit_log.is_finished = True
            audit_log.end_time = now()
            audit_log.save()
        except ObjectDoesNotExist:
            pass
        except AttributeError:
            pass
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
                try:
                    data = api.Api.json_load(text_data)
                    if isinstance(data, dict) and data["tp"] == "init":
                        data = data.get("data")
                        if data.get("sid"):
                            hosts = Hosts.objects.filter(sid=int(data.get("sid")))
                            if len(hosts) == 1:
                                hosts_certificate = hosts[0].certificate.all()
                                if len(hosts_certificate) != 0:
                                    certificate = hosts_certificate[0]
                                else:
                                    query_certificate = Certificate.objects.filter(id=1)
                                    if len(query_certificate) == 1:
                                        certificate = query_certificate[0]
                                    else:
                                        self.send('\033[1;3;31m无法获取主机凭证！\033[0m')
                                        return

                                api.logger.info("connection established from: user={0}, access_ip={1}".format(
                                    self.scope["user"].username, hosts[0].ip
                                ))
                                self.ssh.load_system_host_keys()
                                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                                try:
                                    if certificate.ssh_type == "PASSWORD":
                                        self.ssh.connect(
                                            hostname=hosts[0].ip,
                                            username=certificate.ssh_user,
                                            password=certificate.ssh_password,
                                            port=int(certificate.ssh_port),
                                            timeout=30,
                                            allow_agent=False,
                                            look_for_keys=False
                                        )
                                    elif certificate.ssh_type == "KEY":
                                        private_key = StringIO(certificate.ssh_key)
                                        p_key = get_key_obj(paramiko.RSAKey, pkey_obj=private_key) or \
                                            get_key_obj(paramiko.DSSKey, pkey_obj=private_key) or \
                                            get_key_obj(paramiko.ECDSAKey, pkey_obj=private_key) or \
                                            get_key_obj(paramiko.Ed25519Key, pkey_obj=private_key)

                                        try:
                                            self.ssh.connect(
                                                hostname=hosts[0].ip,
                                                username=certificate.ssh_user,
                                                port=int(certificate.ssh_port),
                                                timeout=30,
                                                password="",
                                                pkey=p_key,
                                                allow_agent=False,
                                                look_for_keys=False
                                            )
                                        except AuthenticationException:
                                            self.ssh.connect(
                                                hostname=hosts[0].ip,
                                                username=certificate.ssh_user,
                                                port=int(certificate.ssh_port),
                                                timeout=30,
                                                password="",
                                                pkey=p_key,
                                                disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]),
                                                allow_agent=False,
                                                look_for_keys=False
                                            )
                                    else:
                                        self.send('\033[1;3;31m无法匹配主机认证类型！\033[0m')
                                        return
                                    audit_log = ConnectRecord.objects.create(
                                        username=User.objects.get(username=self.scope["user"].username),
                                        server=hosts[0],
                                        channel=self.channel_name,
                                        width=data["width"], height=data["height"]
                                    )
                                    audit_log.save()
                                except AuthenticationException:
                                    self.send('\033[1;3;31m认证失败！\033[0m')
                                    return
                                except socket.timeout:
                                    self.send('\033[1;3;31m连接超时！\033[0m')
                                    return
                                except Exception as e:
                                    self.send('\033[1;3;31mCan not connect to server: {0}\033[0m'.format(e))
                                    return

                                self.chan = self.ssh.invoke_shell(
                                    width=data["width"],
                                    height=data["height"],
                                    term='xterm'
                                )

                                directory_date_time = now()
                                log_name = os.path.join('{0}-{1}-{2}'.format(
                                    directory_date_time.year,
                                    directory_date_time.month,
                                    directory_date_time.day), '{0}'.format(audit_log.log)
                                )
                                ssh_interactive = InterActiveShellThread(
                                    self,
                                    self.chan,
                                    log_name=log_name,
                                    width=data["width"],
                                    height=data["height"],
                                    username=self.scope["user"].username
                                )
                                ssh_interactive.setDaemon = True
                                ssh_interactive.start()
                            else:
                                self.send('\033[1;3;31m主机查找不存在！\033[0m')
                                return
                        else:
                            self.send('\033[1;3;31m获取参数错误！\033[0m')
                            return
                    elif isinstance(data, dict) and data["tp"] == "set_size":
                        self.chan.resize_pty(width=data["width"], height=data["height"])
                    elif isinstance(data, dict) and data["tp"] == "close":
                        self.disconnect(0)
                        return
                    else:
                        self.chan.send(data)
                except:
                    if self.chan is not None:
                        self.chan.send(text_data)
                    else:
                        self.close()
            elif bytes_data:
                self.send(bytes_data)
            else:
                self.send(text_data)
        except Exception as e:
            api.logger.error("{0}".format(str(e)))
            self.close()


def get_key_obj(pkeyobj, pkey_file=None, pkey_obj=None):
    if pkey_file:
        with open(pkey_file) as fo:
            try:
                pkey = pkeyobj.from_private_key(fo)
                return pkey
            except:
                pass
    else:
        try:
            pkey = pkeyobj.from_private_key(pkey_obj)
            return pkey
        except:
            pkey_obj.seek(0)
