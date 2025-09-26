from fastapi import APIRouter, Depends
from shared.dependencies import get_currency_service

from modules.finance.adapter.input.api.v1.request import (
	CurrencyCreateRequest,
	CurrencyUpdateRequest,
)

currency_router = APIRouter()


@currency_router.get("")
async def get_all_currencies(
	service = Depends(get_currency_service)
):
	return await service.get_currency_list()


@currency_router.get("/{id_currency}")
async def get_currency_by_id(
	id_currency: int,
	service = Depends(get_currency_service)
):
	return await service.get_currency_by_id(id_currency)


@currency_router.post("")
async def create_currency(
	command: CurrencyCreateRequest,
	service = Depends(get_currency_service)
):
	return await service.create_currency_and_save(command)


@currency_router.put("")
async def update_currency(
	command: CurrencyUpdateRequest,
	service = Depends(get_currency_service)
):
	return await service.update_currency(command)


@currency_router.delete("/{id_currency}")
async def delete_currency(
	id_currency: int,
	service = Depends(get_currency_service)
):
	return await service.delete_currency(id_currency)
