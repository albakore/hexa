"""
Módulo de User Relationships
Configuración simplificada usando variables y funciones
"""

from typing import Dict

from fastapi import APIRouter

from modules.user_relationships.container import UserRelationshipContainer


def setup_routes() -> APIRouter:
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


# Configuración del módulo
name = "user_relationship"
container = UserRelationshipContainer()
service: Dict[str, object] = {
	"user_relationship_service": container.service,
}
routes = setup_routes()
