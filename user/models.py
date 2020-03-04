import datetime

from django.db import models


# Create your models here.
# 用户信息
from vip.models import Vip


class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('广州', '广州'),
        ('深圳', '深圳'),
        ('杭州', '杭州'),
        ('武汉', '武汉'),
        ('成都', '成都'),
        ('重庆', '重庆'),
        ('西安', '西安'),
        ('沈阳', '沈阳'),
    )
    phonenum = models.CharField(max_length=16, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    sex = models.CharField(max_length=8, choices=SEX, verbose_name='性别')
    birthday = models.DateField(default=datetime.date(1996, 5, 20), verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')
    location = models.CharField(max_length=16, choices=LOCATION, verbose_name='常居地')
    vip_id = models.IntegerField(default=1, verbose_name="vip ID")

    # 返回个人资料(不使用外键关联的方式，完成user和profile一对一对应关系)
    @property  # @property将类里面的函数设置为属性，调用时可以不用加括号
    def profile(self):
        # 每次从数据库中取数据都要消耗时间（比如：profile.dating_sex），所以将profile暂存到self中
        # 判断self中是否有profile属性
        if not hasattr(self, '_profile'):
            # 单下划线是指供内部使用
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    # 返回用户对应的vip
    @property
    def vip(self):
        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

    # 返回json数据
    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'phonenum': self.phonenum,
    #         'nickname': self.nickname,
    #         'sex': self.sex,
    #         # date数据类型不能被json序列化,所以给强转成字符串
    #         'birthday': str(self.birthday),
    #         'avatar': self.avatar,
    #         'location': self.location,
    #     }


# 个人中心
class Profile(models.Model):
    dating_sex = models.CharField(max_length=8, choices=User.SEX, verbose_name='匹配的性别')
    dating_location = models.CharField(max_length=16, choices=User.LOCATION, verbose_name='目标城市')

    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=16, verbose_name='最大查找范围')

    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')

    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让为匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='是否自动播放视频')
