import time

import logging

from django.utils.deprecation import MiddlewareMixin

from common import status
from user.models import User
from libs.http import render_json


err_logger = logging.getLogger('err')

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
    # 访问白名单
    PATH_WHITE_LIST = [

        '/api/user/get_vcode',
        '/api/user/check_vcode',
    ]

    def process_request(self, request):
        # 检查请求路径是否在白名单中，如果在就跳过这个中间件
        if request.path in self.PATH_WHITE_LIST:
            return
        # 获取uid
        uid = request.session.get('uid')
        # 如果没有uid就返回LoginRequired码
        if not uid:

            # 通过抛错的形式只能在views函数里面使用，不能在中间件里面使用
            return render_json('LoginRequired', code=status.LoginRequired.code)
        # 获取当前用户
        request.user = User.objects.get(id=uid)


# 逻辑错误中间件
class LogicErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, status.LogicError):
            err_logger.error('API %s CODE %s DATA %s' %(request.path, exception.code, exception.data))
            return render_json(data=exception.data, code=exception.code)

