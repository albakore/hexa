import uuid
from fastapi import APIRouter, Query, Depends
from shared.dependencies import get_draft_invoice_service
from modules.provider.adapter.input.api.v1.request import (
	DraftPurchaseInvoiceCreateRequest,
	DraftPurchaseInvoiceUpdateRequest,
)
from modules.provider.domain.command import (
	CreateDraftPurchaseInvoiceCommand,
	UpdateDraftPurchaseInvoiceCommand,
)

draft_invoice_router = APIRouter()


@draft_invoice_router.get("")
async def get_all_draft_invoices(
	id_provider: int,
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	service = Depends(get_draft_invoice_service),
):
	return await service.get_all_draft_purchase_invoices(id_provider, limit, page)


@draft_invoice_router.get("/{id_draft_invoice}")
async def get_draft_invoice_by_id(
	id_draft_invoice: int,
	service = Depends(get_draft_invoice_service),
):
	invoice = await service.get_draft_purchase_invoice_by_id(id_draft_invoice)
	invoice_with_metadata = await service.get_draft_purchase_invoice_with_filemetadata(
		invoice
	)
	return invoice_with_metadata


@draft_invoice_router.post("")
async def create_draft_invoice(
	command: DraftPurchaseInvoiceCreateRequest,
	service = Depends(get_draft_invoice_service),
):
	draft_invoice = await service.create_draft_purchase_invoice(command)
	return await service.save_draft_purchase_invoice(draft_invoice)


@draft_invoice_router.put("/{id_draft_invoice}")
async def update_draft_invoice(
	id_draft_invoice: int,
	command: DraftPurchaseInvoiceUpdateRequest,
	service = Depends(get_draft_invoice_service),
):
	draft_invoice = UpdateDraftPurchaseInvoiceCommand.model_validate(command)
	draft_invoice_db = await service.get_draft_purchase_invoice_by_id(id_draft_invoice)
	draft_invoice_db.sqlmodel_update(draft_invoice)
	return await service.save_draft_purchase_invoice(draft_invoice_db)


@draft_invoice_router.delete("/{id_draft_invoice}")
async def delete_draft_invoice(
	id_draft_invoice: int,
	service = Depends(get_draft_invoice_service),
):
	return await service.delete_draft_purchase_invoice(id_draft_invoice)


@draft_invoice_router.post("/{id_draft_invoice}/emit")
async def finalize_and_emit_invoice(
	id_draft_invoice: int,
	service = Depends(get_draft_invoice_service),
):
	return await service.finalize_and_emit_invoice(id_draft_invoice)
