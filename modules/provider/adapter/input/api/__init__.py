from fastapi import APIRouter

from modules.provider.adapter.input.api.v1.provider import provider_router as provider_v1_router

router = APIRouter()
router.include_router(
	provider_v1_router,
	prefix="/providers/v1/providers",
	tags=["Providers"]
)
__all__ = [
	"router"
]