import time
from demo_celery_app import app

@app.task
def multiply(x, y):
    time.sleep(2)
    return x * y