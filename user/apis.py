# from django.shortcuts import render
# 因为需要的是json数据，所以不需上面的render，直接导入JsonResponse

# from django.http import JsonResponse
from django.core.cache import cache

from common import keys
from common import status
from user import logics
from libs.http import render_json
from libs.txcloud import upload_to_tx
from user.models import User

from user.forms import UserForm, ProfileForm


# 用户获取验证码
def get_vcode(request):
    phonenum = request.GET.get('phonenum')
    # 逻辑写道logics里面
    # logics调用send_vcode方法
    if logics.send_vcode(phonenum):
        return render_json()
    else:
        raise status.SMSErr
        # return render_json(code=status.SMSErr, data='SMSErr')


# 检查验证码，并进行登录注册
def check_vcode(request):
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    print(vcode)

    # 验证码时间较短，需要将验证码放进缓存里面再来验证
    cached_vcode = cache.get(keys.VCODE_KEY % phonenum)
    # 判断验证码是否过期
    if cached_vcode is None:
        raise status.VcodeExpired
        # return render_json(code=status.VcodeExpired, data='VcodeExpired')
    # 检查验证码是否一致
    if cached_vcode == vcode:
        # 获取或创建对象
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)

        # 使用session记录登录状态
        request.session['uid'] = user.id
        # 将用户信息发送给前端
        return render_json(data=user.to_dict())
    else:
        # return render_json(code=status.VcodeErr, data='VcodeErr')
        raise status.VcodeErr


# 1. 获取交友资料接口
def get_profile(request):
    # 自定义的中间件里面  request.user  <---->  User.objects.get(id=uid)
    # 添加缓存键
    key = keys.PROFILE_KEY % request.user.id
    # 先从缓存里面拿数据
    data = cache.get(key)
    # 如果没有就去数据库里面获取，并存进数据库
    if not data:
        profile = request.user.profile
        data = profile.to_dict()
        cache.set(key, data)
    return render_json(data)


# 2. 修改个人、交友资料接口
def set_profile(request):
    # 将提交的数据放进表单，并初始化
    user_form = UserForm(request.POST)
    user = request.user
    # 判断表单是否有效
    if user_form.is_valid():
        # __dict__ 用来修改类对象的属性值
        user.__dict__.update(user_form.cleaned_data)
        user.save()
    else:
        # 直接抛出实例，手动添加data
        raise status.UserDataErr(user_form.errors)
        # return render_json(data=user_form.errors, code=status.UserDataErr)

    profile_form = ProfileForm(request.POST)
    # profile = user.profile
    if profile_form.is_valid():
        # 当你通过表单获取你的模型数据，但是需要给模型里null=False字段添加一些非表单的数据，该方法会非常有用。如果你指定commit=False，
        # 那么save方法不会理解将表单数据存储到数据库，而是给你返回一个当前对象。这时你可以添加表单以外的额外数据，再一起存储。
        # 生成一个空对象,减少跟数据库通信的次数
        profile = profile_form.save(commit=False)
        profile.id = user.id
        profile.save()
        # 缓存更新
        key = keys.PROFILE_KEY % request.user.id
        # 通过删除缓存达到更新目的，还有就是被动的过期
        # cache.delete(key)
        cache.set(key, profile.to_dict())
    else:
        raise status.ProfileDataErr(profile_form.errors)
        # return render_json(data=profile_form.errors, code=status.ProfileDataErr)

    return render_json()


# 3. 上传个人头像接口
def upload_avatar(request):
    avatar_file = request.FILES['avatar']
    # 调用delay方法接收参数，实现celery异步
    # 打开异步命令pipenv run celery worker -A worker --loglevel=info -P eventlet
    # 需要安装eventlet，不然celery4.*不兼容
    logics.upload_avatar.delay(request.user, avatar_file)
    return render_json()
