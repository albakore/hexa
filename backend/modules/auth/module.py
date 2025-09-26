from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.auth.container import AuthContainer
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app


class AuthModule(ModuleInterface):
	"""Módulo de autenticación desacoplado"""

	def __init__(self):
		self._container = AuthContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "auth"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		routes = get_routes("modules.auth")
		router = APIRouter(prefix="/auth", tags=["Authentication"])
		set_routes_to_app(router, routes)
		return router
