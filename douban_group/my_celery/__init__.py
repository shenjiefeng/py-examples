# encoding: utf-8
__author__ = 'fengshenjie'
from celery import Celery


# 创建 Celery 实例
# mycelery = Celery('douban', include=['util.web'])
mycelery = Celery('douban')
# 通过 Celery 实例加载配置模块
mycelery.config_from_object('my_celery.celeryconfig')
