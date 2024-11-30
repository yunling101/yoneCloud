#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/Users/peng.zou/myWork/myProjects/yoneCloud/webserver')

django.setup()
from webserver.AlarmManage.models import AlarmTemplate


# 模板：生成用于插入数据的脚本内容
generated_template = """#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webserver.settings")
sys.path.append('/yoneCloud/webserver')

django.setup()
from webserver.AlarmManage.models import AlarmTemplate


def main():
    queryset = [
{entries}
    ]
    
    for tpl in queryset:
        template, created = AlarmTemplate.objects.get_or_create(**tpl)
        if created:
            print("AlarmTemplate insert success: " + str(template.id))
        else:
            print("AlarmTemplate insert already exists")


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
    queryset = AlarmTemplate.objects.all().order_by('id')  # 获取所有规则并按照id降序排序
    entries = []

    for perm in queryset:
        field = get_fields(perm)
        entries.append(f'        {field}')

    entries_str = ",\n".join(entries)
    generated_content = generated_template.format(entries=entries_str)

    current_path = os.path.dirname(os.path.abspath(__file__))
    with open("{0}/initialize_alarm_template.py".format(current_path), "w") as f:
        f.write(generated_content)

    print("Generated Python script to insert perm: initialize_alarm_template.py")


if __name__ == "__main__":
    main()
