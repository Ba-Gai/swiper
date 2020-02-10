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
        raise status.SwipeTypeError
        # if stype not in ['like', 'superlike', 'dislike']:
        #     raise status.SwiperTypeError
        # cls.objects.get_or_create(uid=uid, sid=sid)