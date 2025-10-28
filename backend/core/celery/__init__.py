from celery import Celery
from core.config.settings import env

# Crear la aplicación maestra de Celery
celery_app = Celery(
	"hexa_worker",
	broker=env.RABBITMQ_URL,
	backend=env.REDIS_URL,
)
