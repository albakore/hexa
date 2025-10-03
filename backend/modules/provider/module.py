from re import T
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.provider.container import ProviderContainer
from typing import Dict, TypedDict
from modules.user.application.service.user import UserService
from dependency_injector.wiring import Provide


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
	def service(self) -> Dict[str, object]:
		return {
			"provider_service": self._container.provider_service(),
			"draft_invoice_service": self._container.draft_invoice_service(),
		}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.provider import provider_router as provider_v1_router
		from .adapter.input.api.v1.draft_invoice import (
			draft_invoice_router as draft_invoice_v1_router,
		)

		router = APIRouter(prefix="/providers", tags=["Providers"])
		router.include_router(
			provider_v1_router, prefix="/v1/providers", tags=["Providers"]
		)
		router.include_router(
			draft_invoice_v1_router,
			prefix="/v1/draft_invoice",
			tags=["Providers Draft Invoice"],
		)

		return router
