from django.shortcuts import render
# 因为需要的是json数据，所以不需上面的render，直接导入JsonResponse
from django.http import JsonResponse

# Create your views here.


# 获取短信验证码
from common import status
from user import logics


def get_vcode(request):
    # 用户获取验证码
    phonenum = request.GET.get('phonenum')
    # 逻辑写道logics里面
    # logics调用send_vcode方法
    if logics.send_vcode(phonenum):
        return JsonResponse({'code': status.OK, 'data': None})
    else:
        return JsonResponse({'code': status.VcodeErr , 'data': 'VcodeError'})




# 验证验证码
def check_vcode(request):
    return JsonResponse({'code': 1009})