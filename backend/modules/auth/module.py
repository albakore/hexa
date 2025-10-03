from re import T
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.auth.container import AuthContainer
from typing import Dict, TypedDict
from modules.user.application.service.user import UserService
from dependency_injector.wiring import Provide


class AuthModule(ModuleInterface):
	"""Módulo de autenticacion desacoplado"""

	def __init__(self):
		self._container = AuthContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "auth"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def service(self) -> Dict[str, object]:
		return {
			"auth_service": self._container.service(),
			"auth.jwt_service": self._container.jwt_service(),
		}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.auth import auth_router as auth_v1_router

		router = APIRouter(prefix="/auth", tags=["Authentication"])
		router.include_router(
			auth_v1_router, prefix="/v1/auth", tags=["Authentication"]
		)

		return router
