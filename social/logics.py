import datetime
from django.core.cache import cache

from common import keys, status
from social.models import Swiper
from swiper import config
from user.models import User, Profile
from social.models import Friend


# 添加用户推荐，并且需要排除已经滑过的用户
def rcmd(user):
    today = datetime.date.today()
    max_birthday = today - datetime.timedelta(user.profile.min_dating_age * 365)
    min_birthday = today - datetime.timedelta(user.profile.max_dating_age * 365)

    swipe_ids = Swiper.swipe_uid_list(user.id)

    users = User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.dating_location,
        birthday__lte=max_birthday,
        birthday__gte=min_birthday,
    ).exclude(id__in=swipe_ids)[:20]  # 排除掉id在已经滑过id的用户，一次只拿20个用户
    return users


# 喜欢某人
def like_someone(user, sid):
    # 添加滑动记录
    Swiper.swipe(user.id, sid, 'like')
    # 检查对方是否喜欢过自己，如果互相喜欢就配对成好友
    if Swiper.is_like(sid, user.id):
        Friend.make_friend(user.id, sid)
        return True
    else:
        return False


# 喜欢某人
def superlike_someone(user, sid):
    # 添加滑动记录
    Swiper.swipe(user.id, sid, 'superlike')
    # 检查对方是否喜欢过自己，如果互相喜欢就配对成好友
    if Swiper.is_like(sid, user.id):
        Friend.make_friend(user.id, sid)
        return True
    else:
        return False


# 反悔
def rewind_swipe(user):
    # 检查当天是否超过指定次数
    key = keys.REMIND_KEY % user.id
    # 取出当前剩余次数
    remain_times = cache.get(key, config.DAILY_REMIND)
    if remain_times <= 0:
        raise status.RewindLimited
    # 取出最后滑动记录
    latest_swipe = Swiper.objects.filter(uid=user.id).latest('stime')
    # 检查上一次滑动是否在5分钟之内
    now = datetime.datetime.now()  # 当前时间
    if (now - latest_swipe.stime).total_seconds() > config.REMIND_TIMEOUT:
        raise status.RewindTimeOut
    # 检查是否曾经匹配成好友，如果是撤销好友关系
    if latest_swipe.stype in ['like', 'superlike']:
        Friend.break_off(user.id, latest_swipe.sid)
    # 删除滑动记录
    latest_swipe.delete()
    # 重新计算并记录剩余次数
    # 下一个零点时间
    next_zero = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
    # 到凌晨的剩余时间，total_seconds()获得秒数
    expire_seconds = (next_zero - now).total_seconds()
    # 重新写入缓存
    remain_times -= 1
    cache.set(key, remain_times, expire_seconds)