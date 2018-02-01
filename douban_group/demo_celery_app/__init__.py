# encoding: utf-8
__author__ = 'fengshenjie'
from celery import Celery

app = Celery('demo')  # 创建 Celery 实例
app.config_from_object('demo_celery_app.celeryconfig')  # 通过 Celery 实例加载配置模块

# ref: https://segmentfault.com/a/1190000007780963