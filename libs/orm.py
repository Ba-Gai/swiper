# 自定义一个model_to_dict(将model转化成字典)
from datetime import date, time, datetime


# 类比from django.forms import form中的model_to_dict
def model_to_dict(model_obj, ignore=()):
    # 定义字典
    attr_dict = {}
    # 遍历model文件拿到对应的name和value
    for field in model_obj._meta.fields:
        name = field.attname
        if name not in ignore:
            value = getattr(model_obj, name)
            # 检查value能否被json序列化
            if isinstance(value, (datetime, time, date)):
                value = str(value)
            attr_dict[name] = value
    return attr_dict
