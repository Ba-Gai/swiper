import datetime
from django.core.cache import cache

from common import keys, status
from social.models import Swiper
from swiper import config
from user.models import User, Profile
from social.models import Friend
from libs.cache import rds


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
    # 反悔后减去已添加的积分
    score = -config.SWIPE_SCORE[latest_swipe]
    rds.zincrby('HotRank', score, latest_swipe.sid)
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


def liked_me(user):
    like_stype = ['like', 'superlike']
    # 好友id列表
    friend_id_list = Friend.friend_ids(user.id)
    # 喜欢我的id列表
    liked_me_id_list = Swiper.objects.filter(sid=user.id, stype__in=like_stype).exclude(
        uid__in=friend_id_list).values_list('uid', flat=True)
    # 拿到喜欢过我的用户id列表
    users = User.objects.filter(id__in=liked_me_id_list)
    return users


# 添加积分
def add_score(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        # 获取sid
        sid = request.POST.get('sid')
        # 获取函数名
        stype = view_func.__name__
        # 获取积分
        score = config.SWIPE_SCORE[stype]
        # 修改积分
        rds.zincrby(keys.RANK_KEY, score, sid)
        return response
    return wrapper

# 获取排名前N的用户范围
def get_top_n(num):
    # 取出并且清洗数据
    origin_data = rds.zrevrange(keys.RANK_KEY, 0, num-1, withscores=True)
    # 将取出的数据改成int类型
    cleaned = [[int(uid), int(score)] for uid, score in origin_data]
    # 取出每一个用户
    user_list = [i[0] for i in cleaned]
    users = User.objects.filter(id__in=user_list)
    # 取出的数据是按照user的id升序排列的，需要重新定义sorted方法
    users = sorted(users, key=lambda user : user_list.index(user.id))
    rank_data = {}
    # enumerate 可以返回users里面的index
    for idx, user in enumerate(users):
        # 返回user信息
        user_info = user.to_dict()
        # 计算排名
        rank = idx + 1
        # 添加积分，值是cleaned里对应排名的索引为1的
        user_info['score'] = cleaned[idx][1]
        # 添加rank，值是user_info
        rank_data[rank] = user_info
    return rank_data