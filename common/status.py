'''系统状态码'''

OK = 0
SMSErr = 1000  # 发送验证码错误
VcodeExpired = 1001  # 验证码已过期
VcodeErr = 1002  # 验证码错误
LoginRequired = 1003  # 需要用户登录
UserDataErr = 1004  # 用户信息错误
ProfileDataErr = 1005  # 交友个人资料信息错误
