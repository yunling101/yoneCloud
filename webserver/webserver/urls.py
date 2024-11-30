#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken import views

from django.conf import settings
admin.autodiscover()

schema_view = get_swagger_view(title='Yone Cloud API')
v1_api_patterns = [
    url('v1/', include('webserver.ResourceManage.api_urls', namespace='api-asset')),
    url('v1/', include('webserver.UserManage.api_urls', namespace='api-user')),
    url('v1/', include('webserver.BusinessManage.api_urls', namespace='api-business')),
    url('v1/', include('webserver.AuditManage.api_urls', namespace='api-audit')),
    url('v1/', include('webserver.TaskManage.api_urls', namespace='api-task')),
    url('v1/', include('webserver.JobsManage.api_urls', namespace='api-jobs')),
    url('v1/', include('webserver.AuthManage.api_urls', namespace='api-auth')),
    url('v1/', include('webserver.SystemManage.api_urls', namespace='api-system')),
    url('v1/', include('webserver.AlarmManage.api_urls', namespace='api-alarm')),
]

urlpatterns = [
    url(r'', include('webserver.website.urls')),
    url(r'', include('webserver.UserManage.urls')),
    url(r'', include('webserver.SystemManage.urls')),
    url(r'', include('webserver.AuditManage.urls')),
    url(r'', include('webserver.UserManage.urls')),
    url(r'', include('webserver.ResourceManage.urls')),
    url(r'', include('webserver.BusinessManage.urls')),
    url(r'', include('webserver.EventManage.urls')),
    url(r'', include('webserver.AlarmManage.urls')),
    url(r'', include('webserver.TaskManage.urls')),
    url(r'', include('webserver.AuthManage.urls')),
    url(r'', include('webserver.JobsManage.urls')),

    url(r'api/', include(v1_api_patterns)),
    url(r'api/api-token-auth/', views.obtain_auth_token),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.ENV_DOCS == "true":
    urlpatterns += [
        url('api/docs/', schema_view, name="api-docs"),
    ]

handler404 = "webserver.common.views.http404"
handler500 = "webserver.common.views.http500"
