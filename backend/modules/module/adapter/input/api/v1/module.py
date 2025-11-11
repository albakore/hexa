from dependency_injector.wiring import Provide, inject
from fastapi import (
	APIRouter,
	Depends,
	Query,
)

from modules.module.application.service.module import AppModuleService

from modules.module.container import AppModuleContainer
# from core.fastapi.dependencies.module_permission.module import ModuleTokenPermission

module_router = APIRouter()


@module_router.get(
	"",
	# dependencies=[ModuleTokenPermission.read]
)
@inject
# @TokenRegistry.register("module:read")
async def get_app_module_list(
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	module_service: AppModuleService = Depends(Provide[AppModuleContainer.service]),
):
	return await module_service.get_module_list(int(limit), int(page))
