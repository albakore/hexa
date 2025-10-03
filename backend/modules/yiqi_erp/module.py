from re import T
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.yiqi_erp.container import YiqiContainer
from typing import Dict


class YiqiERPModule(ModuleInterface):
	"""Módulo de Yiqi ERP desacoplado"""

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
	def service(self) -> Dict[str, object]:
		return {"yiqi_erp_service": self._container.service()}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.yiqi_erp import yiqi_erp_router as yiqi_erp_v1_router

		router = APIRouter(prefix="/yiqi_erp", tags=["Yiqi ERP"])
		router.include_router(
			yiqi_erp_v1_router, prefix="/v1/yiqi_erp", tags=["Yiqi ERP"]
		)

		return router
