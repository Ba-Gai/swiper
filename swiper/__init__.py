import pymysql
# 将自己底层的接口伪装成mysql的
pymysql.install_as_MySQLdb()