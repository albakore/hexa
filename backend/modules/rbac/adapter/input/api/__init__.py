from fastapi import APIRouter

from modules.rbac.adapter.input.api.v1.rbac import rbac_router as rbac_v1_router

router = APIRouter()
router.include_router(rbac_v1_router, prefix="/rbac/v1/rbac", tags=["RBAC"])
__all__ = ["router"]
