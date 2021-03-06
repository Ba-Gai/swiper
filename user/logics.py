import os
import random
import requests
from django.core.cache import cache

from libs.txcloud import upload_to_tx
from swiper import config
from common import keys
from django.conf import settings
from worker import  celery_app


# 生成指定长度的随机验证码
def random_code(length=6):
    return "".join([str(random.randint(0, 9)) for i in range(length)])


# 发送验证码
def send_vcode(phonenum):
    vcode = random_code()
    print(vcode)
    # 将验证码记录到缓存,时间到自动过期
    cache.set(keys.VCODE_KEY % phonenum, vcode, 180)
    # 每个用户访问的都是自己函数生成的params文件，不会大量的去修改全局变量，从而导致线程a安全问题
    params = config.YZX_PARAMS.copy()
    params["param"] = vcode
    params["mobile"] = phonenum
    resp = requests.post(config.YZX_API, json=params)
    if resp.status_code == 200:
        return True
    else:
        return False


# 上传文件到服务器，并临时存放
def save_avatar(upload_file, uid):
    filename = 'Avatar-%s' % uid
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    with open(filepath, 'wb') as fp:
        # chunk 将文件切分上传，减轻上传服务器压力
        for chunk in upload_file.chunks():
            fp.write(chunk)

    return filename, filepath

@celery_app.task
def upload_avatar(user, avatar_file):
    # 上传到服务器，返回文件名称和路径
    filename, filepath = save_avatar(avatar_file, user.id)
    # 图片上传到腾讯对象存储
    avatar_url = upload_to_tx(filename, filepath)
    # 删除本地文件
    os.remove(filepath)
    # 将文件保存到数据库
    user.avatar = avatar_url
    user.save()