#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/Users/peng.zou/myWork/myProjects/yoneCloud/webserver')

django.setup()
from webserver.UserManage.models import Permission


# 模板：生成用于插入数据的脚本内容
generated_template = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.UserManage.models import Permission


def main():
    queryset = [
{entries}
    ]
    
    for perm in queryset:
        permission, created = Permission.objects.get_or_create(**perm)
        if created:
            print("Permission insert success: " + str(permission.id))
        else:
            print("Permission insert already exists")


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
    queryset = Permission.objects.all().order_by('id')  # 获取所有规则并按照id降序排序
    entries = []

    for perm in queryset:
        field = get_fields(perm)
        entries.append(f'        {field}')

    entries_str = ",\n".join(entries)
    generated_content = generated_template.format(entries=entries_str)

    current_path = os.path.dirname(os.path.abspath(__file__))
    with open("{0}/initialize_perm.py".format(current_path), "w") as f:
        f.write(generated_content)

    print("Generated Python script to insert perm: initialize_perm.py")


if __name__ == "__main__":
    main()
