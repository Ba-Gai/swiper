import os
from celery import Celery
from worker import config

# celery和django不是一个进程
# 加载django配置settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")


celery_app = Celery('worker')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()

