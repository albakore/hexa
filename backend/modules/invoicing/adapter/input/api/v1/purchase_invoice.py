from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Query, Response

from modules.invoicing.adapter.input.api.v1.request import CreatePurchaseInvoiceRequest
from modules.invoicing.container import InvoicingContainer
from shared.interfaces.service_locator import service_locator

# from modules.invoicing.adapter.input.api.v1.request import (
# 	ProviderCreateRequest,
# 	ProviderUpdateRequest,
# )
from modules.invoicing.application.service.purchase_invoice import (
	PurchaseInvoiceService,
)


purchase_invoice_router = APIRouter()


@purchase_invoice_router.get("")
@inject
async def get_all_purchase_invoices(
	limit: int = Query(default=50, ge=1, le=100),
	page: int = Query(default=0),
	service: PurchaseInvoiceService = Depends(
		Provide[InvoicingContainer.purchase_invoice_service]
	),
):
	return await service.get_list(limit, page)


@purchase_invoice_router.get("/of_provider/{id_provider}")
@inject
async def get_all_purchase_invoices_of_provider(
	id_provider: int,
	limit: int = Query(default=50, ge=1, le=100),
	page: int = Query(default=0),
	service: PurchaseInvoiceService = Depends(
		Provide[InvoicingContainer.purchase_invoice_service]
	),
):
	return await service.get_list_of_provider(id_provider, limit, page)


@purchase_invoice_router.get("/{id_purchase_invoice}")
@inject
async def get_purchase_invoices_by_id(
	id_purchase_invoice: int,
	service: PurchaseInvoiceService = Depends(
		Provide[InvoicingContainer.purchase_invoice_service]
	),
):
	return await service.get_one_by_id(id_purchase_invoice)


@purchase_invoice_router.post("")
@inject
async def create_purchase_invoice(
	purchase_invoice: CreatePurchaseInvoiceRequest,
	emit_to_yiqi: bool,
	service: PurchaseInvoiceService = Depends(
		Provide[InvoicingContainer.purchase_invoice_service]
	),
):
	invoice = await service.create(purchase_invoice)
	invoice_saved = await service.save(invoice)

	# Ejecutar task de Celery de forma asíncrona si se solicita
	if emit_to_yiqi:
		yiqi_tasks = service_locator.get_service("yiqi_erp_tasks")
		yiqi_tasks["emit_invoice"].delay(invoice_saved.model_dump())

	return invoice_saved
