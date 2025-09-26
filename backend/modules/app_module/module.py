from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.app_module.container import AppModuleContainer
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app


class AppModuleModule(ModuleInterface):
	"""Módulo de aplicación desacoplado"""

	def __init__(self):
		self._container = AppModuleContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "app_module"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		routes = get_routes("modules.app_module")
		router = APIRouter(prefix="/modules", tags=["App Modules"])
		set_routes_to_app(router, routes)
		return router
