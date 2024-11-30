#!/usr/bin/env python
# -*- coding:utf-8 -*-

# AuthMiddlewareStack组合了AuthMiddleware, SessionMiddleware和CookieMiddleware

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from webserver.consumer import routing

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})
