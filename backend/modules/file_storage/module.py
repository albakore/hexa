"""
Módulo de File Storage
Configuración simplificada usando variables y funciones
"""

from typing import Dict

from fastapi import APIRouter

from modules.file_storage.container import FileStorageContainer


def setup_routes() -> APIRouter:
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


# Configuración del módulo
name = "file_storage"
container = FileStorageContainer()
service: Dict[str, object] = {
	"file_storage_service": container.service,
}
routes = setup_routes()
