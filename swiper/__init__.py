import pymysql
from libs.orm import patch_model

# 将自己底层的接口伪装成mysql的
pymysql.install_as_MySQLdb()
# 为model添加缓存层
patch_model()