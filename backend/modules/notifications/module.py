
from typing import Any, Dict
from dependency_injector.containers import DeclarativeContainer
from fastapi.routing import APIRouter
from modules.notifications.container import NotificationsContainer
from shared.interfaces.module_registry import ModuleInterface


class NotificationModule(ModuleInterface):
	"""Módulo de usuarios desacoplado"""

	def __init__(self):
		self._container = NotificationsContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "notifications"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def service(self) -> Dict[str, object]:
		return {"notifications_service": self._container.service}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.notifications import notifications_router as notifications_v1_router

		router = APIRouter(prefix="/notifications", tags=["Notifications"])
		router.include_router(notifications_v1_router, prefix="/v1/notifications")

		return router