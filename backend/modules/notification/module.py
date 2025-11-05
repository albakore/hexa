from typing import Dict
from dependency_injector.containers import DeclarativeContainer
from fastapi.routing import APIRouter
from modules.notification.adapter.input.tasks.notification import (
	send_notification_tasks,
)
from modules.notification.container import NotificationContainer
from shared.interfaces.module_registry import ModuleInterface


class NotificationModule(ModuleInterface):
	"""Módulo de notificaciones desacoplado"""

	def __init__(self):
		self._container = NotificationContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "notification"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def service(self) -> Dict[str, object]:
		return {
			"notification_service": self._container.service,
			"email_template_service": self._container.email_template_service,
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

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.notification import (
			notifications_router as notifications_v1_router,
		)
		from .adapter.input.api.v1.email_template import (
			email_templates_router as email_templates_v1_router,
		)

		router = APIRouter(prefix="/notifications", tags=["Notifications"])
		router.include_router(notifications_v1_router, prefix="/v1/notifications")
		router.include_router(email_templates_v1_router, prefix="/v1/email_templates")
		return router
