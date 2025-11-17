from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.finance.container import FinanceContainer
from typing import Dict


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
	def service(self) -> Dict[str, object]:
		return {"currency_service": self._container.currency_service}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.currency import currency_router as currency_v1_router

		router = APIRouter(prefix="/finance", tags=["Finance"])
		router.include_router(
			currency_v1_router, prefix="/v1/currency", tags=["Finance"]
		)

		return router
