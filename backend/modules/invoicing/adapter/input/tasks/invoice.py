import time
from celery import Celery
from core.config.settings import env

celery_worker_name = "invoicing"

app = Celery(
	celery_worker_name,
	broker=env.RABBITMQ_URL,
	backend=env.REDIS_URL,
)


@app.task
def my_task_invoice():
	time.sleep(10)
	return "Hola desde celery!!!"
