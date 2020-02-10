from libs.http import render_json
from social import logics


# 推荐用户
def rcmd_users(request):
    # 拿到过滤用户列表
    users = logics.rcmd(request.user)
    result = [user.to_dict() for user in users ]
    return render_json(result)


# 喜欢的右滑
def like(request):
    sid = int(request.POST.get('sid'))
    logics.like_someone(request.user, sid)
    return render_json()


# 超级喜欢上滑
def superlike(request):
    return render_json()

# 不喜欢左滑
def dislike(request):
    return render_json()


# 反悔
def rewind(request):
    return render_json()


# 查看喜欢过我的人
def show_liked_me(request):
    return render_json()


# 好友列表
def friend_list(request):
    return render_json()
