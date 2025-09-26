from fastapi import APIRouter, Query, Depends
from shared.dependencies import get_provider_service

from modules.provider.adapter.input.api.v1.request import (
	ProviderCreateRequest,
	ProviderUpdateRequest,
)

provider_router = APIRouter()


@provider_router.get("")
async def get_all_providers(
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	service = Depends(get_provider_service),
):
	return await service.get_all_providers(limit, page)


@provider_router.get("/{id_provider}")
async def get_provider_by_id(
	id_provider: int,
	service = Depends(get_provider_service),
):
	return await service.get_provider_by_id(id_provider)


@provider_router.post("")
async def create_provider(
	command: ProviderCreateRequest,
	service = Depends(get_provider_service),
):
	provider = await service.create_provider(command)
	return await service.save_provider(provider)


@provider_router.put("")
async def update_provider(
	command: ProviderUpdateRequest,
	service = Depends(get_provider_service),
):
	return await service.update_provider(command)


@provider_router.delete("/{id_provider}")
async def delete_provider(
	id_provider: int,
	service = Depends(get_provider_service),
):
	return await service.delete_provider(id_provider)
