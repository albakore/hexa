from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.finance.container import FinanceContainer
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app


class FinanceModule(ModuleInterface):
	"""Módulo de finanzas desacoplado"""

	def __init__(self):
		self._container = FinanceContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "finance"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		routes = get_routes("modules.finance")
		router = APIRouter(prefix="/finance", tags=["Finance"])
		set_routes_to_app(router, routes)
		return router
