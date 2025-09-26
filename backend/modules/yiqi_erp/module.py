from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.yiqi_erp.container import YiqiContainer
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app


class YiqiERPModule(ModuleInterface):
	"""Módulo de YiQi ERP desacoplado"""

	def __init__(self):
		self._container = YiqiContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "yiqi_erp"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		routes = get_routes("modules.yiqi_erp")
		router = APIRouter(prefix="/yiqi", tags=["YiQi ERP"])
		set_routes_to_app(router, routes)
		return router
