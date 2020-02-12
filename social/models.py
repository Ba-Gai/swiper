from django.db import models
from common import status

# 添加滑动信息model
class Swiper(models.Model):
    STYPE = (
        ('like', '右滑'),
        ('superlike', '上滑'),
        ('dislike', '左滑'),
    )

    uid = models.IntegerField(verbose_name="滑动者的id")
    sid = models.IntegerField(verbose_name="被滑动者的id")
    stype = models.CharField(max_length=10, choices=STYPE,verbose_name="滑动方式")
    stime = models.DateTimeField(auto_now_add=True, verbose_name="滑动时间")

    @classmethod
    def swipe(cls, uid, sid, stype):
        # 执行一次滑动并记录
        if stype not in ['like', 'superlike', 'dislike']:
            raise status.SwipeTypeError
        if cls.objects.filter(uid=uid, sid=sid).exists():
            raise status.SwipeThisOneError
        return cls.objects.create(uid=uid, sid=sid, stype=stype)

    # 检查是否喜欢过某人
    @classmethod
    def is_like(cls, uid, sid):
        like_stypes = ['like', 'superlike']
        # __in: 判断stype是否在like_stypes列表里面
        return cls.objects.filter(uid=uid, sid=sid, stype__in=like_stypes).exists()

    # 记录滑动列表
    @classmethod
    def swipe_uid_list(cls, uid):
        return cls.objects.filter(uid=uid).values_list('sid', flat=True)

# 好友关系表
class Friend(models.Model):

    uid1 = models.IntegerField(verbose_name="好友ID")
    uid2 = models.IntegerField(verbose_name="好友ID")

    # 建立好友关系
    @classmethod
    def make_friend(cls, uid1, uid2):
        # 判断一下大小，方便操作
        uid1, uid2 = (uid1, uid2) if uid1< uid2 else (uid2, uid1)
        cls.objects.get_or_create(uid1=uid1, uid2=uid2)
