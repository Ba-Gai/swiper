from libs.http import render_json
from social import logics
from social.models import Swiper, Friend
from user.models import User
import logging

# 添加日志对象
from vip.logics import need_perm

inf_logger = logging.getLogger('inf')

def rcmd_users(request):
    # 拿到过滤用户列表
    users = logics.rcmd(request.user)
    result = [user.to_dict() for user in users]
    return render_json(result)


# 喜欢的右滑
@logics.add_score
def like(request):
    sid = int(request.POST.get('sid'))
    # 是否匹配成好友
    is_matched = logics.like_someone(request.user, sid)
    # 写入日志
    inf_logger.info('%s like %s' %(request.user.id, sid))
    return render_json({'is_matched': is_matched})


# 超级喜欢上滑
@need_perm('superlike')
@logics.add_score
def superlike(request):
    sid = int(request.POST.get('sid'))
    # 是否匹配成好友
    is_matched = logics.superlike_someone(request.user, sid)
    inf_logger.info('%s superlike %s' % (request.user.id, sid))
    return render_json({'is_matched': is_matched})


# 不喜欢左滑
@logics.add_score
def dislike(request):
    sid = int(request.POST.get('sid'))
    # 添加滑动记录
    Swiper.swipe(request.user.id, sid, 'dislike')
    inf_logger.info('%s dislike %s' % (request.user.id, sid))
    return render_json()


# 接口设计的一些原则：
#      吝啬原则（参数或者返回值能少既少）；
#      安全原则（客户端传来的任何东西都不可信，任何参数都需要检查，即使这个值在前端有检查）
# 反悔
@need_perm('rewind')
def rewind(request):
    logics.rewind_swipe(request.user)
    return render_json()


# 查看喜欢过我的人
@need_perm('show_liked_me')
def show_liked_me(request):
    # 喜欢过我的用户
    users = logics.liked_me(request.user)
    # 获取这些用户的详细信息
    result = [user.to_dict() for user in users]
    return render_json(result)


# 好友列表
def friend_list(request):
    friend_id_list = Friend.friend_ids(request.user.id)
    users = User.objects.filter(id__in=friend_id_list)
    result = [user.to_dict() for user in users]
    return render_json(result)
