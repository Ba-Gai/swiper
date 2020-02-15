# 程序逻辑配置，及第三方平台配置

# 云之讯短信平台配置
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
    'templateid': '485815',
    'param': None,
    'mobile': None,
}

# 七牛云配置
QN_BUCKET = 'ding-01'
QN_BASEURL = 'http://puvot7qe4.bkt.clouddn.com'
QN_ACCESSKEY = 'FB3609sMvURurQr7s_j8oJPLUkv1RoZCE_QHjjTi'
QN_SECRETKEY = 'WjV_aLvXXR48uCW22nfIIbCU76h7OQXnFJ4n9tFS'

# 腾讯云对象存储配置
# id 和 key写你自己的
secret_id = 'secret_id'  # secret_id
secret_key = 'secret_key'  # secret_key
Bucket = 'avatar-1259234619',
PartSize = 1,
MAXThread = 10,
EnableMD5 = False
BaseUrl = 'https://avatar-1259234619.cos.ap-chengdu.myqcloud.com'
region = 'ap-chengdu'

# 每日反悔次数
DAILY_REMIND = 3
# 只能反悔五分钟之内的操作
REMIND_TIMEOUT = 5 * 60
