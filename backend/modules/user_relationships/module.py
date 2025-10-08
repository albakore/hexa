from re import T
from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.user_relationships.container import UserRelationshipContainer
from typing import Dict


class UserRelationshipsModule(ModuleInterface):
	"""Módulo de relationes de usuarios desacoplado"""

	def __init__(self):
		self._container = UserRelationshipContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "user_relationship"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def service(self) -> Dict[str, object]:
		return {"user_relationship_service": self._container.service}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.user_relationship import (
			user_relationship_router as user_relationship_v1_router,
		)

		router = APIRouter(prefix="/user_relationship", tags=["User Relationships"])
		router.include_router(
			user_relationship_v1_router,
			prefix="/v1/user_relationship",
			tags=["User Relationships"],
		)

		return router
