from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.provider.container import ProviderContainer
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app


class ProviderModule(ModuleInterface):
	"""Módulo de proveedores desacoplado"""

	def __init__(self):
		self._container = ProviderContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "provider"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		routes = get_routes("modules.provider")
		router = APIRouter(prefix="/providers", tags=["Providers"])
		set_routes_to_app(router, routes)
		return router
