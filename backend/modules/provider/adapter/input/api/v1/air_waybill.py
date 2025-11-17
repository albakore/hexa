import json
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Form

from modules.provider.adapter.input.api.v1.request import (
	AirWaybillCreateRequest,
	AirWaybillUpdateRequest,
)
from modules.provider.application.service.air_waybill import AirWaybillService
from modules.provider.container import ProviderContainer
from modules.provider.domain.command import UpdateAirWaybillCommand


air_waybill_router = APIRouter()


@air_waybill_router.get("")
@inject
async def get_all_air_waybills(
	id_invoice: int,
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	service: AirWaybillService = Depends(
		Provide[ProviderContainer.air_waybill_service]
	),
):
	return await service.get_all_air_waybills(id_invoice, limit, page)


@air_waybill_router.get("/{id_air_waybill}")
@inject
async def get_air_waybill_by_id(
	id_air_waybill: int,
	service: AirWaybillService = Depends(
		Provide[ProviderContainer.air_waybill_service]
	),
):
	return await service.get_air_waybill_by_id(id_air_waybill)


@air_waybill_router.post("")
@inject
async def create_air_waybill(
	command: AirWaybillCreateRequest,
	service: AirWaybillService = Depends(
		Provide[ProviderContainer.air_waybill_service]
	),
):
	air_waybill = await service.create_air_waybill(command)
	print(air_waybill)
	return await service.save_air_waybill(air_waybill)


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
