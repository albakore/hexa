from fastapi import APIRouter

from modules.provider.adapter.input.api.v1.provider import (
	provider_router as provider_v1_router,
)
from modules.provider.adapter.input.api.v1.draft_invoice import (
	draft_invoice_router as draft_invoice_v1_router,
)
from modules.provider.adapter.input.api.v1.purchase_invoice_service import (
	purchase_invoice_service_router as purchase_invoice_service_v1_router,
)

router = APIRouter()
router.include_router(
	provider_v1_router, prefix="/providers/v1/providers", tags=["Providers"]
)
router.include_router(
	draft_invoice_v1_router,
	prefix="/providers/v1/draft_invoice",
	tags=["Providers Draft Invoice"],
)
router.include_router(
	purchase_invoice_service_v1_router,
	prefix="/providers/v1/purchase_invoice_service",
	tags=["Providers Invoice Services"],
)
__all__ = ["router"]
