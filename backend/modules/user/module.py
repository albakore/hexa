from fastapi import APIRouter

from modules.user.container import UserContainer


def setup_routes() -> APIRouter:
	"""Configura las rutas del módulo"""
	from .adapter.input.api.v1.user import user_router as user_v1_router

	router = APIRouter(prefix="/users", tags=["Users"])
	router.include_router(user_v1_router, prefix="/v1/users", tags=["Users"])

	return router


name = "user"
container = UserContainer()
service = {
	"user_service": container.service,
}
routes = setup_routes()
