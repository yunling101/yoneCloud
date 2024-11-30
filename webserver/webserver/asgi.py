"""
ASGI config for webserver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django

from channels.routing import get_default_application
from django.conf import settings

# settings.configure()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
from webserver.settings import RD_HOST, RD_PORT
settings.ASGI_APPLICATION = "webserver.routing.application"
settings.INSTALLED_APPS.append("channels")
settings.CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(RD_HOST, RD_PORT)],
        },
    }
}

django.setup()
application = get_default_application()
