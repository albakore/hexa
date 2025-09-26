from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.user.container import UserContainer
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app


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
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		routes = get_routes("modules.user")
		router = APIRouter(prefix="/users", tags=["Users"])
		set_routes_to_app(router, routes)
		return router
