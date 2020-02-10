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
        return cls.objects.get_or_create(uid=uid, sid=sid, stype=stype)

    # 检查是否喜欢过某人
    @classmethod
    def is_like(cls, uid, sid):
        like_stypes = ['like', 'superlike']
        # __in: 判断stype是否在like_stypes列表里面
        return cls.objects.filter(uid=uid, sid=sid, stype__in=like_stypes).exists()

    @classmethod
    def swipe_uid_list(cls, uid):
        return cls.objects.filter(uid=uid).values_list('sid', flat=True)