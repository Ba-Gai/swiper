# 自定义一个model_to_dict(将model转化成字典)
from datetime import date, time, datetime
from django.db import models

from common.keys import MODEL_KEY
from libs.cache import rds


# 类比from django.forms import form中的model_to_dict
def model_to_dict(self, ignore=()):
    # 定义字典
    attr_dict = {}
    # 遍历model文件拿到对应的name和value
    for field in self._meta.fields:
        name = field.attname
        if name not in ignore:
            value = getattr(self, name)
            # 检查value能否被json序列化
            if isinstance(value, (datetime, time, date)):
                value = str(value)
            attr_dict[name] = value
    return attr_dict


def save_with_cache(self, force_insert=False, force_update=False, using=None,
                    update_fields=None):
    """
    Saves the current instance. Override this in a subclass if you want to
    control the saving process.

    The 'force_insert' and 'force_update' parameters can be used to insist
    that the "save" must be an SQL insert or update (or equivalent for
    non-SQL backends), respectively. Normally, they should not be set.
    """
    # Ensure that a model instance without a PK hasn't been assigned to
    # a ForeignKey or OneToOneField on this model. If the field is
    # nullable, allowing the save() would result in silent data loss.

    # 执行原来的save方法
    # 将数据存到数据库里面
    result = self._save(force_insert, force_update, using,
                        update_fields)
    # print("已经保存到数据库")
    # 将数据存到缓存里面
    key = MODEL_KEY % (self.__class__.__name__, self.pk)
    rds.set(key, self)
    # print("已经保存到缓存")
    return result


def get_with_cache(self, *args, **kwargs):
    """
    Performs the query and returns a single object matching the given
    keyword arguments.
    """
    # 先检查参数中有没有id或者主键
    pk = kwargs.get('id') or kwargs.get('pk')
    cls_name = self.model._meta.object_name
    if pk:
        # 构造缓存key
        key = MODEL_KEY % (cls_name, pk)
        # 从缓存获取model_obj对象
        model_obj = rds.get(key)
        if isinstance(model_obj, self.model):
            return model_obj
    # 缓存没有就去数据库获取数据，调用原来的get方法
    model_obj = self._get(*args, **kwargs)
    # 添加到缓存
    key = MODEL_KEY % (cls_name, model_obj.pk)
    rds.set(key, model_obj)
    return model_obj

# 通过MonkeyPatch的方式为model添加缓存处理
def patch_model():
    # 先将原来的save方法保存，起别名
    models.Model._save = models.Model.save
    # MonkeyPatch 猴子补丁，动态改变方法
    models.Model.save = save_with_cache

    models.query.QuerySet._get = models.query.QuerySet.get
    models.query.QuerySet.get = get_with_cache

    # 为model添加to_dict方法
    models.Model.to_dict = model_to_dict
