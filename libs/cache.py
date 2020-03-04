from redis import Redis as _Redis
from pickle import dumps, loads, HIGHEST_PROTOCOL, UnpicklingError
from swiper.config import REDIS


# 自定义redis缓存
class Redis(_Redis):
    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        # HIGHEST_PROTOCOL  速度最快
        # 添加了pickle处理的 set
        pickled = dumps(value, HIGHEST_PROTOCOL)
        return super().set(name, pickled, ex, px, nx, xx)

    def get(self, name):
        # 添加了反序列化的get
        pickled = super().get(name)
        try:
            return loads(pickled)
        except (UnpicklingError, TypeError):
            return pickled


# 实例化redis对象（单例）
rds = Redis(**REDIS)
