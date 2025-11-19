from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from modules.provider.adapter.input.api.v1.request import (
	LinkPurchaseInvoiceServiceToProviderRequest,
	PurchaseInvoiceServiceCreateRequest,
	PurchaseInvoiceServiceUpdateRequest,
)
from modules.provider.application.service.purchase_invoice_service import (
	PurchaseInvoiceServiceTypeService,
)
from modules.provider.container import ProviderContainer

purchase_invoice_service_router = APIRouter()


@purchase_invoice_service_router.get("")
@inject
async def get_all_services(
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	return await service.get_all_services(limit, page)


@purchase_invoice_service_router.get("/{id_purchase_invoice_service}")
@inject
async def get_service_by_id(
	id_purchase_invoice_service: int,
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	return await service.get_services_by_id(id_purchase_invoice_service)


@purchase_invoice_service_router.post("")
@inject
async def create_service(
	command: PurchaseInvoiceServiceCreateRequest,
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	new_command = await service.create_purchase_invoice_service(command)
	service = await service.save_purchase_invoice_service(new_command)
	return service


@purchase_invoice_service_router.get("/get-from/provider/{id_provider}")
@inject
async def get_services_of_provider(
	id_provider: int,
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	return await service.get_services_of_provider(id_provider)


@purchase_invoice_service_router.post("/add-to/provider/{id_provider}")
@inject
async def add_services_to_provider(
	id_provider: int,
	services: List[LinkPurchaseInvoiceServiceToProviderRequest],
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	return await service.add_services_to_provider(id_provider, services)


@purchase_invoice_service_router.delete("/remove-from/provider/{id_provider}")
@inject
async def remove_services_from_provider(
	id_provider: int,
	id_services_list: List[int],
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	return await service.remove_services_from_provider(id_provider, id_services_list)


@purchase_invoice_service_router.put("")
@inject
async def update_service(
	command: PurchaseInvoiceServiceUpdateRequest,
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	service_updated = await service.update_purchase_invoice_service(command)
	return service_updated


@purchase_invoice_service_router.delete("/{id_purchase_invoice_service}")
@inject
async def delete_service(
	id_purchase_invoice_service: int,
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	service_updated = await service.delete_purchase_invoice_service(
		id_purchase_invoice_service
	)
	return service_updated
