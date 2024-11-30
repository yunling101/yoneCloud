#!/usr/bin/env python
# -*- coding:utf-8 -*-

provider = {
    "腾讯云": {
        "resources": ["hosts", "cdn", "domain", "mysql", "redis", "mongodb"]
    },
    "阿里云": {
        "resources": ["hosts", "cdn", "domain", "mysql", "redis", "mongodb"]
    },
    "亚马逊": {
        "resources": ["hosts"]
    },
    "百度云": {
        "resources": ["hosts"]
    },
    "华为云": {
        "resources": ["hosts"]
    },
    "UCLOUD": {
        "resources": ["hosts", "mysql", "redis", "mongodb"]
    },
    "物理机": {
        "resources": []
    },
    "私有云": {
        "resources": []
    },
    "虚拟机": {
        "resources": []
    },
    "其他": {
        "resources": []
    }
}
