from django.db import models


# 会员
class Vip(models.Model):
    name = models.CharField(max_length=16, unique=True, verbose_name="vip名称")
    level = models.IntegerField(verbose_name="vip等级")
    price = models.FloatField(verbose_name="vip价格")


# 权限
class Permission(models.Model):
    name = models.CharField(max_length=16, unique=True, verbose_name="权限名称")
    desc = models.TextField(verbose_name="权限描述")


# 会员和权限的关系
class VipPermRelation(models.Model):
    vip_id = models.IntegerField(verbose_name="vip ID")
    perm_id = models.IntegerField(verbose_name="权限 ID")
