import datetime
from user.models import User, Profile


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
