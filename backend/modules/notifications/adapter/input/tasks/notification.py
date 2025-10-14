from celery import Celery
from core.config.settings import env

celery_worker_name = "notifications"
app = Celery(
	name=celery_worker_name,
	broker=env.RABBITMQ_URL,
	backend=env.REDIS_URL,
)


@app.task()
def my_task_notification():
	return "Esto es una notificacion"
