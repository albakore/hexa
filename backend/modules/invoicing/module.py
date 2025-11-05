from typing import Dict

from dependency_injector.containers import DeclarativeContainer
from fastapi import APIRouter

from modules.invoicing.container import InvoicingContainer
from shared.interfaces.module_registry import ModuleInterface


class InvoicingModule(ModuleInterface):
	"""Módulo de invoicing desacoplado"""

	def __init__(self):
		self._container = InvoicingContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "invoicing"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def service(self) -> Dict[str, object]:
		return {"purchase_invoice_service": self._container.purchase_invoice_service}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.purchase_invoice import (
			purchase_invoice_router as purchase_invoice_v1_router,
		)

		router = APIRouter(prefix="/invoicing", tags=["Invoicing"])
		router.include_router(purchase_invoice_v1_router, prefix="/v1/purchase_invoice")

		return router
