#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import DefaultSchema


class Schema(object):
    def __init__(self, description):
        self.description = description
        self.field = []

    def push(self, name=None, required=False, location="form", t="string", description=None):
        self.field.append(coreapi.Field(
            name=name,
            required=required,
            location=location,
            type=t,
            schema=coreschema.String(
                title=name,
                description=description,
            ),
        ))

    def schema(self):
        if coreapi is not None and coreschema is not None:
            return ManualSchema(
                fields=self.field,
                description=self.description,
                encoding="application/json",
            )
        else:
            return DefaultSchema


# 对model app field 进行object， 测试代码
class ModelField(object):
    @classmethod
    def field(cls, app, no_show=None):
        field_obj = {}
        for f in app:
            if f.name not in no_show:
                field_obj[f.name] = {
                    "verbose_name": f.verbose_name,
                    "description": f.description,
                    "null": f.null,
                    "type": type(f).__name__,
                }
        # print(field_obj)
