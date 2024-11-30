#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/Users/peng.zou/myWork/myProjects/yoneCloud/webserver')

django.setup()
from webserver.UserManage.models import Permission, Role


# 模板：生成用于插入数据的脚本内容
generated_template = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.UserManage.models import Permission, Role


def main():
    entries = {{"id": 1, "name": "\u9ed8\u8ba4\u89d2\u8272", "comment": ""}}
    
    permission = [
{permission}
    ]
    
    role, created = Role.objects.get_or_create(**entries)
    if created:
        permission_select = []
        for perm in permission:
            view = Permission.objects.filter(view=perm["view"])
            if len(view) == 1:
                permission_select.append(view[0])
        role.permission.set(permission_select)
        role.save()
        
        print("Role insert success: " + str(role.id))
    else:
        print("Role insert already exists")

    
if __name__ == "__main__":
    main()

"""


def get_fields(instance):
    """获取模型实例的所有字段和值，返回字典形式"""
    field_dict = {}
    for field in instance._meta.fields:
        field_name = field.name
        field_value = getattr(instance, field_name)
        field_dict[field_name] = field_value
    return field_dict


def main():
    queryset = Role.objects.filter(name="默认角色")
    permission = []

    for role in queryset:
        for perm in role.permission.all():
            field_perm = get_fields(perm)
            permission.append(f'        {field_perm}')

    permission_str = ",\n".join(permission)
    generated_content = generated_template.format(permission=permission_str)

    current_path = os.path.dirname(os.path.abspath(__file__))
    with open("{0}/initialize_role.py".format(current_path), "w") as f:
        f.write(generated_content)

    print("Generated Python script to insert role: initialize_role.py")


if __name__ == "__main__":
    main()
