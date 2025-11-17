from fastapi import APIRouter

from modules.finance.adapter.input.api.v1.currency import (
	currency_router as currency_v1_router,
)

router = APIRouter()
router.include_router(
	currency_v1_router, prefix="/finance/v1/currency", tags=["Finance"]
)

__all__ = ["router"]
