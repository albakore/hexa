from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Query, Response

from modules.container import ModuleContainer
from modules.provider.application.service.provider import ProviderService




provider_router = APIRouter()

@provider_router.get("")
@inject
async def get_all_providers(
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	service : ProviderService = Depends(Provide[ModuleContainer.provider.service])
):
	return await service.get_all_providers(limit,page)