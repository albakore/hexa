from re import T
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.user.container import UserContainer
from typing import Dict


class UserModule(ModuleInterface):
	"""Módulo de usuarios desacoplado"""

	def __init__(self):
		self._container = UserContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "user"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def service(self) -> Dict[str, object]:
		return {"user_service": self._container.service()}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.user import user_router as user_v1_router

		router = APIRouter(prefix="/users", tags=["Users"])
		router.include_router(user_v1_router, prefix="/users/v1/users", tags=["Users"])

		return router
