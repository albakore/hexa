from fastapi import APIRouter

from modules.auth.adapter.input.api.v1.auth import auth_router as auth_v1_router

router = APIRouter()
router.include_router(
	auth_v1_router,
	prefix="/auth/v1/auth",
	tags=["Auth"]
)
__all__ = [
	"router"
]