from celery import Celery
from celery.utils.log import get_task_logger

REDIS_BASE_URL = 'redis://localhost:6379'
logger = get_task_logger(__name__)

app = Celery('task', 
             backend=REDIS_BASE_URL,
             broker=REDIS_BASE_URL
            )

@app.task()
def collect_data():
    pass
