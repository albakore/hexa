"""
Módulo de RBAC (Role Based Access Control)
Configuración simplificada usando variables y funciones
"""

from typing import Dict

from fastapi import APIRouter

from modules.rbac.container import RBACContainer


def setup_routes() -> APIRouter:
	"""Configura las rutas del módulo"""
	from .adapter.input.api.v1.rbac import rbac_router as rbac_v1_router

	router = APIRouter(prefix="/rbac", tags=["RBAC Role Based Access Control"])
	router.include_router(
		rbac_v1_router, prefix="/v1/rbac", tags=["RBAC Role Based Access Control"]
	)

	return router


# Configuración del módulo
name = "rbac"
container = RBACContainer()
service: Dict[str, object] = {
	"rbac.role_service": container.role_service,
	"rbac.permission_service": container.permission_service,
}
routes = setup_routes()
