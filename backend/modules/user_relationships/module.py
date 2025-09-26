from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.user_relationships.container import UserRelationshipContainer
from core.fastapi.server.route_helpers import get_routes, set_routes_to_app


class UserRelationshipModule(ModuleInterface):
	"""Módulo de relaciones de usuarios desacoplado"""

	def __init__(self):
		self._container = UserRelationshipContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "user_relationships"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		routes = get_routes("modules.user_relationships")
		router = APIRouter(prefix="/user-relationships", tags=["User Relationships"])
		set_routes_to_app(router, routes)
		return router
