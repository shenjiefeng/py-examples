import time
from demo_celery_app import app

@app.task
def add(x, y):
    time.sleep(2)
    return x + y