from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.rbac.container import RBACContainer
from typing import Dict


class RBACModule(ModuleInterface):
	"""Módulo de roles y permisos desacoplado"""

	def __init__(self):
		self._container = RBACContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "rbac"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def service(self) -> Dict[str, object]:
		return {
			"rbac.role_service": self._container.role_service,
			"rbac.permission_service": self._container.permission_service,
		}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.rbac import rbac_router as rbac_v1_router

		router = APIRouter(prefix="/rbac", tags=["RBAC Role Based Access Control"])
		router.include_router(
			rbac_v1_router, prefix="/v1/rbac", tags=["RBAC Role Based Access Control"]
		)

		return router
