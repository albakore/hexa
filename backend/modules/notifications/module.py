from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from typing import Dict


class NotificationsModule(ModuleInterface):
	"""Módulo de Notifications desacoplado"""

	def __init__(self):
		# Este módulo solo tiene tasks, no tiene container ni rutas por ahora
		pass

	@property
	def name(self) -> str:
		return "notifications"

	@property
	def container(self) -> DeclarativeContainer | None:
		return None

	@property
	def service(self) -> Dict[str, object]:
		# Importar las tasks como funciones normales
		from .adapter.input.tasks import notification

		return {
			# Exponer las tasks como un dict de callables
			"notifications_tasks": {
				"send_notification": notification.send_notification,
			},
		}

	@property
	def routes(self) -> APIRouter:
		# Este módulo no tiene rutas HTTP por ahora
		return APIRouter(prefix="/notifications", tags=["Notifications"])