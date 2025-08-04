import uuid
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from modules.container import ModuleContainer
from modules.provider.container import DraftPurchaseInvoiceService


draft_invoice_router = APIRouter()


@draft_invoice_router.get("/{id_provider}")
@inject
async def get_all_draft_invoices(
	id_provider: int,
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	service: DraftPurchaseInvoiceService = Depends(
		Provide[ModuleContainer.provider.draft_invoice_service]
	)
):
	return await service.get_all_draft_purchase_invoices(id_provider, limit, page)
