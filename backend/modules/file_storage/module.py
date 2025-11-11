from fastapi import APIRouter
from dependency_injector.containers import DeclarativeContainer

from shared.interfaces.module_registry import ModuleInterface
from modules.file_storage.container import FileStorageContainer
from typing import Dict


class FileStorageModule(ModuleInterface):
	"""Módulo de Almacenamiento de archivos desacoplado"""

	def __init__(self):
		self._container = FileStorageContainer()
		self._routes = self._setup_routes()

	@property
	def name(self) -> str:
		return "file_storage"

	@property
	def container(self) -> DeclarativeContainer:
		return self._container

	@property
	def service(self) -> Dict[str, object]:
		return {"file_storage_service": self._container.service}

	@property
	def routes(self) -> APIRouter:
		return self._routes

	def _setup_routes(self) -> APIRouter:
		"""Configura las rutas del módulo"""
		from .adapter.input.api.v1.file_storage import (
			file_storage_router as file_storage_v1_router,
		)

		router = APIRouter(prefix="/filestorage", tags=["File Storage Service"])
		router.include_router(
			file_storage_v1_router,
			prefix="/v1/filestorage",
			tags=["File Storage Service"],
		)

		return router
