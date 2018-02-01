from datetime import timedelta
from celery.schedules import crontab
from util.web import update_ips


BROKER_URL = 'redis://127.0.0.1:6378'               # 指定 Broker
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6378/0'  # 指定 Backend

CELERY_TIMEZONE='Asia/Shanghai'                     # 指定时区，默认是 UTC
# CELERY_TIMEZONE='UTC'

CELERY_IMPORTS = (                                  # 指定导入的任务模块
    'util.web'
)

# 定时任务
CELERYBEAT_SCHEDULE = {
    'run-every-x-minute': {
         'task': 'util.web.update_ips',
         'schedule': timedelta(seconds=4*60),
         'args': ('ip.txt',)
    },
    # 'run-at-some-time': {
    #     'task': 'util.web.update_ips',
    #     'schedule': crontab(hour=9, minute=50),   # 每天早上 9 点 50 分执行一次
    #     'args': ('ip.txt',)                            # 任务函数参数
    # }
}