from celery import Celery
from core.config.settings import env

celery_app = Celery(backend=env.REDIS_URL, broker=env.RABBITMQ_URL)
