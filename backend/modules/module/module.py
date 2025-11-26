"""
Módulo de App Module
Configuración simplificada usando variables y funciones
"""

from typing import Dict

from fastapi import APIRouter

from modules.module.container import AppModuleContainer


def setup_routes() -> APIRouter:
	"""Configura las rutas del módulo"""
	from .adapter.input.api.v1.module import module_router as module_v1_router

	router = APIRouter(prefix="/modules", tags=["App Module"])
	router.include_router(module_v1_router, prefix="/v1/modules", tags=["App Module"])

	return router


# Configuración del módulo
name = "app_module"
container = AppModuleContainer()
service: Dict[str, object] = {
	"app_module_service": container.service,
	# Excepción: Se expone el repositorio para RBAC porque Role tiene relación M:N con Module
	# Esto es una dependencia de dominio legítima (aggregate roots relacionados)
	"app_module.repository_adapter": container.repository_adapter,
}
routes = setup_routes()
