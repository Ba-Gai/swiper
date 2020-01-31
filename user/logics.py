import random
import requests

from swiper import config

# 生成指定长度的随机验证码
def random_code(length=6):
    return "".join([str(random.randint(0, 9)) for i in range(length)])

# 发送验证码
def send_vcode(phonenum):
    vcode = random_code()
    print(vcode)
    # 每个用户访问的都是自己函数生成的params文件，不会大量的去修改全局变量，从而导致线程a安全问题
    params = config.YZX_PARAMS.copy()
    params["param"] = vcode
    params["mobile"] = phonenum
    resp = requests.post(config.YZX_API, json=params)
    if resp.status_code == 200:
        return True
    else:
        return False

