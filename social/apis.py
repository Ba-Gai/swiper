from libs.http import render_json
from social import logics


# 推荐用户
from social.models import Swiper


def rcmd_users(request):
    # 拿到过滤用户列表
    users = logics.rcmd(request.user)
    result = [user.to_dict() for user in users ]
    return render_json(result)


# 喜欢的右滑
def like(request):
    sid = int(request.POST.get('sid'))
    # 是否匹配成好友
    is_matched = logics.like_someone(request.user, sid)
    return render_json({'is_matched':is_matched})


# 超级喜欢上滑
def superlike(request):
    sid = int(request.POST.get('sid'))
    # 是否匹配成好友
    is_matched = logics.superlike_someone(request.user, sid)
    return render_json({'is_matched':is_matched})

# 不喜欢左滑
def dislike(request):
    sid = int(request.POST.get('sid'))
    # 添加滑动记录
    Swiper.swipe(request.user.id, sid, 'dislike')
    return render_json()


# 接口设计的一些原则：
#      吝啬原则（参数或者返回值能少既少）；
#      安全原则（客户端传来的任何东西都不可信，任何参数都需要检查，即使这个值在前端有检查）
# 反悔
def rewind(request):
    logics.rewind_swipe(request.user)
    return render_json()


# 查看喜欢过我的人
def show_liked_me(request):
    return render_json()


# 好友列表
def friend_list(request):
    return render_json()
