# -*- coding: utf-8 -*-

from demo_celery_app import task1
from demo_celery_app import task2
import time

def run_async_task():
    task1.add.apply_async(args=[2, 8])  # 也可用 task1.add.delay(2, 8)
    res2 = task2.multiply.apply_async(args=[3, 7])
    print('Wating for result……')
    while True:
        if res2.ready():
            print('res2:', res2.get())
            break
        else:
            time.sleep(1)

def run_schedule_task():
    import subprocess
    # 启动worker进程
    p1=subprocess.Popen('celery -A demo_celery_app worker -l info')
    # 启动beat进程
    p2=subprocess.Popen('celery beat -A demo_celery_app')
    # 合一
    p3=subprocess.Popen('celery -B -A demo_celery_app worker --loglevel=info')


if __name__ == '__main__':
    # 1. 启动celery worker
    # celery worker -A celery_app --loglevel=info
    # 2. 调用任务
    run_async_task()
