#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.urls import path
from . import batch, ssh

websocket_urlpatterns = [
    path("ws/batch/", batch.BatchCommand),
    path("ws/ssh/", ssh.WebTerminal),
]
