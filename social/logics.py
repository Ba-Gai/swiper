import datetime

from social.models import Swiper
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
