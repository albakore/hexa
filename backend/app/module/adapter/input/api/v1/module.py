from typing import Annotated
import uuid
from dependency_injector.wiring import Provide, inject
from fastapi import (
	APIRouter,
	Cookie,
	Depends,
	Query,
	WebSocket,
	WebSocketException,
	status,
)

from app.module.application.service.module import AppModuleService
from app.container import SystemContainer

from app.module.container import AppModuleContainer
from core.fastapi.dependencies import PermissionDependency
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
	module_service: AppModuleService = Depends(
		Provide[SystemContainer.app_module.service]
	),
):
	return await module_service.get_module_list(int(limit), int(page))
