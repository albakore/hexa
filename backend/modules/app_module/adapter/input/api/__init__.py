from fastapi import APIRouter

from modules.app_module.adapter.input.api.v1.module import (
	module_router as module_v1_router,
)

router = APIRouter()
router.include_router(
	module_v1_router, prefix="/modules/v1/modules", tags=["App Modules"]
)
__all__ = ["router"]
