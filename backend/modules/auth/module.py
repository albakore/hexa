"""
Módulo de autenticación
Configuración simplificada usando variables y funciones
"""

from typing import Dict

from fastapi import APIRouter

from modules.auth.container import AuthContainer


def setup_routes() -> APIRouter:
	"""Configura las rutas del módulo"""
	from .adapter.input.api.v1.auth import auth_router as auth_v1_router

	router = APIRouter(prefix="/auth", tags=["Authentication"])
	router.include_router(auth_v1_router, prefix="/v1/auth", tags=["Authentication"])

	return router


# Configuración del módulo
name = "auth"
container = AuthContainer()
service: Dict[str, object] = {
	"auth_service": container.service,
	"auth.jwt_service": container.jwt_service,
}
routes = setup_routes()
