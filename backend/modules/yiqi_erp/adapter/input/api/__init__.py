from fastapi import APIRouter

from modules.yiqi_erp.adapter.input.api.v1.yiqi_erp import (
	yiqi_erp_router as yiqi_erp_v1_router,
)

router = APIRouter()
router.include_router(
	yiqi_erp_v1_router, prefix="/yiqi_erp/v1/yiqi_erp", tags=["Yiqi ERP"]
)
__all__ = ["router"]
