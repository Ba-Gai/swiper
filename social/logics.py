import datetime

from social.models import Swiper
from user.models import User, Profile
from libs.http import render_json


# 用户推荐
def rcmd(user):
    today = datetime.date.today()
    max_birthday = today - datetime.timedelta(user.profile.min_dating_age * 365)
    min_birthday = today - datetime.timedelta(user.profile.max_dating_age * 365)

    users = User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.dating_location,
        birthday__lte=max_birthday,
        birthday__gte=min_birthday,
    )[:20]
    # TODO: 需要排除已经滑过的用户

    return users


# 喜欢某人
def like_someone(user, sid):
    Swiper.swipe(user.id, sid, 'like')
    # return render_json()
