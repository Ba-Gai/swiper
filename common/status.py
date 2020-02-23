'''系统状态码'''


#
# OK = 0
# SMSErr = 1000  # 发送验证码错误
# VcodeExpired = 1001  # 验证码已过期
# VcodeErr = 1002  # 验证码错误
# LoginRequired = 1003  # 需要用户登录
# UserDataErr = 1004  # 用户信息错误
# ProfileDataErr = 1005  # 交友个人资料信息错误


# 通过抛错的形式传递错误data和code
class LogicError(Exception):
    code = 0

    def __init__(self, data=None):
        # 如果传进来data就是用data，没有就使用类名
        self.data = data or self.__class__.__name__


# 封装创建错误类函数
def gen_login_err(name, code):
    # 使用元类type创建类
    return type(name, (LogicError, object), {'code': code})


SMSErr = gen_login_err('SMSErr', 1000)  # 发送验证码错误
VcodeExpired = gen_login_err('VcodeExpired', 1001)  # 验证码已过期
VcodeErr = gen_login_err('VcodeErr', 1002)  # 验证码错误
LoginRequired = gen_login_err('LoginRequired', 1003)  # 需要用户登录
UserDataErr = gen_login_err('UserDataErr', 1004)  # 用户信息错误
ProfileDataErr = gen_login_err('ProfileDataErr', 1005)  # 交友个人资料信息错误
SwipeTypeError = gen_login_err('SwipeTypeError', 1006)  # 滑动类型错误
SwipeThisOneError = gen_login_err('SwipeThisOneError', 1007)  # 重复滑动某一个人
RewindLimited = gen_login_err('RewindLimited', 1008)  # 反悔超过默认次数
RewindTimeOut = gen_login_err('RewindTimeOut', 1009)  # 反悔超过默认时间
PermLimited = gen_login_err('PermLimited', 1010)  # 没有权限
