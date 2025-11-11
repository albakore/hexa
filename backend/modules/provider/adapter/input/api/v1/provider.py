from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from modules.provider.container import ProviderContainer
from modules.provider.adapter.input.api.v1.request import (
	ProviderCreateRequest,
	ProviderUpdateRequest,
)
from modules.provider.application.service.provider import ProviderService


provider_router = APIRouter()


@provider_router.get("")
@inject
async def get_all_providers(
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	return await service.get_all_providers(limit, page)


@provider_router.get("/{id_provider}")
@inject
async def get_provider_by_id(
	id_provider: int,
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	return await service.get_provider_by_id(id_provider)


@provider_router.post("")
@inject
async def create_provider(
	command: ProviderCreateRequest,
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	provider = await service.create_provider(command)
	return await service.save_provider(provider)


@provider_router.put("")
@inject
async def update_provider(
	command: ProviderUpdateRequest,
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	return await service.update_provider(command)


@provider_router.delete("/{id_provider}")
@inject
async def delete_provider(
	id_provider: int,
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	return await service.delete_provider(id_provider)
