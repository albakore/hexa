from fastapi import APIRouter

from app.user_relationships.adapter.input.api.v1.user_relationship import user_relationship_router as user_relationship_v1_router

router = APIRouter()
router.include_router(
	user_relationship_v1_router,
	prefix="/user_relationship/v1/user_relationship",
	tags=["User Relationships"]
)
__all__ = [
	"router"
]