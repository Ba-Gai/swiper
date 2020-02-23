from common import status

# 判断是否有权限 装饰器函数
def need_perm(perm_name):
    def inner1(view_fun):
        def inner2(request, *args, **kwargs):
            if request.user.vip.has_perm(perm_name):
                response = view_fun(request, *args, **kwargs)
                return response
            else:
                raise status.PermLimited
        return inner2
    return inner1