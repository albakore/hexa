from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Query, Response

from modules.container import ModuleContainer
from modules.finance.adapter.input.api.v1.request import (
	CurrencyCreateRequest,
	CurrencyUpdateRequest,
)
from modules.finance.application.service.currency import CurrencyService


currency_router = APIRouter()


@currency_router.get("")
@inject
async def get_all_currencies(
	service: CurrencyService = Depends(
		Provide[ModuleContainer.finance.currency_service]
	),
):
	return await service.get_currency_list()


@currency_router.get("/{id_currency}")
@inject
async def get_currency_by_id(
	id_currency: int,
	service: CurrencyService = Depends(
		Provide[ModuleContainer.finance.currency_service]
	),
):
	return await service.get_currency_by_id(id_currency)


@currency_router.post("")
@inject
async def create_currency(
	command: CurrencyCreateRequest,
	service: CurrencyService = Depends(
		Provide[ModuleContainer.finance.currency_service]
	),
):
	return await service.create_currency_and_save(command)


@currency_router.put("")
@inject
async def update_currency(
	command: CurrencyUpdateRequest,
	service: CurrencyService = Depends(
		Provide[ModuleContainer.finance.currency_service]
	),
):
	return await service.update_currency(command)


@currency_router.delete("/{id_currency}")
@inject
async def delete_currency(
	id_currency: int,
	service: CurrencyService = Depends(
		Provide[ModuleContainer.finance.currency_service]
	),
):
	return await service.delete_currency(id_currency)
