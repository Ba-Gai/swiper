# 程序逻辑配置，及第三方平台配置

# 云之讯短信平台配置
import os

YZX_API = 'https://open.ucpaas.com/ol/sms/sendsms'
# YZX_PARAMS = {
#     'sid': os.environ.get("uid"),
#     'token': os.environ.get("token"),
#     'appid': os.environ.get("appid"),
#     'templateid': os.environ.get("templateid"),
#     'param': None,
#     'mobile': None,
# }

YZX_PARAMS = {
    'sid': 'd4ae2ed11b3658e3ecc70948c0851c6d',
    'token': '057aff6f139**********7aa6dec492e',
    'appid': '771fe3ac275943f7924c1ef365fdbd09',
    'templateid': '485814',
    'param': None,
    'mobile': None,
}



# 七牛云配置
QN_BUCKET = 'ding-01'
QN_BASEURL = 'http://puvot7qe4.bkt.clouddn.com'
QN_ACCESSKEY = 'FB3609sMvURurQr7s_j8oJPLUkv1RoZCE_QHjjTi'
QN_SECRETKEY = 'WjV_aLvXXR48uCW22nfIIbCU76h7OQXnFJ4n9tFS'