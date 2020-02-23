from django.db import models


# 会员
class Vip(models.Model):
    name = models.CharField(max_length=16, unique=True, verbose_name="vip名称")
    level = models.IntegerField(verbose_name="vip等级")
    price = models.FloatField(verbose_name="vip价格")

    # vip对应的权限
    def perms(self):
        perm_id_list = VipPermRelation.objects.filter(vip_id=self.id).values_list('perm_id', flat=True)
        return Permission.objects.filter(id__in=perm_id_list)

    # 检查是否有某种权限
    def has_perm(self, perm_name):
        for perm in self.perms():
            if perm.name == perm_name:
                return True
        return False

# 权限
class Permission(models.Model):
    name = models.CharField(max_length=16, unique=True, verbose_name="权限名称")
    desc = models.TextField(verbose_name="权限描述")


# 会员和权限的关系
class VipPermRelation(models.Model):
    vip_id = models.IntegerField(verbose_name="vip ID")
    perm_id = models.IntegerField(verbose_name="权限 ID")
