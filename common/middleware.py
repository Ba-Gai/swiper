import time

from django.utils.deprecation import MiddlewareMixin

from common import status
from user.models import User
from libs.http import render_json


def timer(func):
    '''时间检查装饰器'''
    def warp(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        used = (t2 - t1) * 1000
        print('接口耗时: %0.2f ms' % used)
        return res
    return warp


class AuthMiddleware(MiddlewareMixin):
    PATH_WHITE_LIST = [
        '/user/get_code/',
        '/user/check_code/',
    ]

    def process_request(self, request):
        # 检查当前访问的路径是否在白名单中
        if request.path in self.PATH_WHITE_LIST:
            return

        uid = request.session.get('uid')  # 从 session 中取出 uid
        if not uid:
            # 检查 session 中是否已存在 uid
            return render_json('LoginRequired', code=status.LoginRequired)

        # 获取当前用户
        request.user = User.objects.get(id=uid)
