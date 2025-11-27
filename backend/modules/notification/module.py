"""
Módulo de Notifications
Configuración simplificada usando variables y funciones
"""

from typing import Dict

from fastapi import APIRouter

from modules.notification.adapter.input.tasks.notification import (
	send_notification_tasks,
)
from modules.notification.container import NotificationContainer


def setup_routes() -> APIRouter:
	"""Configura las rutas del módulo"""
	from .adapter.input.api.v1.email_template import (
		email_templates_router as email_templates_v1_router,
	)
	from .adapter.input.api.v1.notification import (
		notifications_router as notifications_v1_router,
	)

	router = APIRouter(prefix="/notifications", tags=["Notifications"])
	router.include_router(notifications_v1_router, prefix="/v1/notifications")
	router.include_router(email_templates_v1_router, prefix="/v1/email_templates")

	return router


# Configuración del módulo
name = "notification"
container = NotificationContainer()
service: Dict[str, object] = {
	"notification_service": container.service,
	"email_template_service": container.email_template_service,
	"notification_tasks": {
		"send_notification_tasks": {
			"task": send_notification_tasks,
			"config": {
				"autoretry_for": (Exception,),
				"retry_kwargs": {"max_retries": 5},
				"retry_backoff": True,
				"retry_backoff_max": 600,
				"retry_jitter": True,
			},
		}
	},
}
routes = setup_routes()
