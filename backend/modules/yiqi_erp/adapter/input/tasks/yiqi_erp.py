import time
from celery import Celery
from core.config.settings import env

celery_worker_name = "yiqi_erp"

app = Celery(
	celery_worker_name,
	broker=env.RABBITMQ_URL,
	backend=env.REDIS_URL,
)


@app.task
def emit_invoice(data):
	print(data)
	return f"YIQI ERP: Hola desde celery!!!"
