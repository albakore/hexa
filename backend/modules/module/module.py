from re import T
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.module.container import AppModuleContainer
from typing import Dict


class AppModuleModule(ModuleInterface):
	"""Módulo de modulo_aplicacion desacoplado"""

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
	def service(self) -> Dict[str, object]:
		return {"app_module_service": self._container.service()}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.module import module_router as module_v1_router

		router = APIRouter(prefix="/modules", tags=["App Module"])
		router.include_router(
			module_v1_router, prefix="/v1/modules", tags=["App Module"]
		)

		return router
