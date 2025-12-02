from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from modules.provider.adapter.input.api.v1.request import (
	AirWaybillCreateRequest,
	AirWaybillUpdateRequest,
)
from modules.provider.application.service.air_waybill import AirWaybillService
from modules.provider.container import ProviderContainer
from modules.provider.domain.command import UpdateAirWaybillCommand


air_waybill_router = APIRouter()


@air_waybill_router.get("/{id_air_waybill}")
@inject
async def get_air_waybill_by_id(
	id_air_waybill: int,
	service: AirWaybillService = Depends(
		Provide[ProviderContainer.air_waybill_service]
	),
):
	return await service.get_air_waybill_by_id(id_air_waybill)


@air_waybill_router.get("/by_draft_invoice/{id_draft_invoice}")
@inject
async def get_air_waybills_by_draft_invoice_id(
	id_draft_invoice: int,
	service: AirWaybillService = Depends(
		Provide[ProviderContainer.air_waybill_service]
	),
):
	return await service.get_air_waybills_by_draft_invoice_id(id_draft_invoice)


@air_waybill_router.get("/by_purchase_invoice/{id_purchase_invoice}")
@inject
async def get_air_waybills_by_purchase_invoice_id(
	id_purchase_invoice: int,
	service: AirWaybillService = Depends(
		Provide[ProviderContainer.air_waybill_service]
	),
):
	return await service.get_air_waybills_by_purchase_invoice_id(id_purchase_invoice)


@air_waybill_router.post("")
@inject
async def create_air_waybills(
	command: list[AirWaybillCreateRequest],
	service: AirWaybillService = Depends(
		Provide[ProviderContainer.air_waybill_service]
	),
):
	air_waybills = await service.create_air_waybills(command)
	print(air_waybills)

	# Validate each air waybill for duplicates
	for air_waybill in air_waybills:
		await service.validate_duplicated_air_waybill(air_waybill)

	# Save all air waybills
	saved_air_waybills = []
	for air_waybill in air_waybills:
		saved = await service.save_air_waybill(air_waybill)
		saved_air_waybills.append(saved)

	return saved_air_waybills


@air_waybill_router.put("/{id_air_waybill}")
@inject
async def update_air_waybill(
	id_air_waybill: int,
	command: AirWaybillUpdateRequest,
	service: AirWaybillService = Depends(
		Provide[ProviderContainer.air_waybill_service]
	),
):
	air_waybill = UpdateAirWaybillCommand.model_validate(
		command.model_dump(exclude_unset=True)
	)
	air_waybill_db = await service.get_air_waybill_by_id(id_air_waybill)
	air_waybill_db.sqlmodel_update(air_waybill)
	return await service.save_air_waybill(air_waybill_db)


@air_waybill_router.delete("/{id_air_waybill}")
@inject
async def delete_air_waybill(
	id_air_waybill: int,
	service: AirWaybillService = Depends(
		Provide[ProviderContainer.air_waybill_service]
	),
):
	return await service.delete_air_waybill(id_air_waybill)
