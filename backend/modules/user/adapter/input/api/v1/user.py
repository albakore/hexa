from typing import Annotated, List
import uuid
from dependency_injector.wiring import Provide, inject
from fastapi import (
	APIRouter,
	Depends,
	Query,
)

from modules.user.container import UserContainer
from shared.interfaces.service_locator import service_locator
from modules.user.adapter.input.api.v1.request import CreateUserRequest, RoleRequest
from modules.user.application.service.user import UserService
from modules.user.domain.command import CreateUserCommand

from core.fastapi.dependencies import PermissionDependency
from core.fastapi.dependencies.user_permission.user import UserTokenPermission

DepUserService = Annotated[UserService, Depends(Provide[UserContainer.service])]
DepRBACService = Depends(lambda: service_locator.get_service("rbac.role_service"))
DepAppModuleService = Depends(lambda: service_locator.get_service("app_module_service"))


user_router = APIRouter()


@user_router.get(
	"",
	# dependencies=[UserTokenPermission.read]
)
@inject
# @TokenRegistry.register("user:read")
async def get_user_list(
	user_service: DepUserService,
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
):
	return await user_service.get_user_list(int(limit), int(page))


@user_router.get(
	"/search",
	# dependencies=[UserTokenPermission.read]
)
@inject
# @TokenRegistry.register("user:read")
async def search_users(
	user_service: DepUserService,
	token_modules: list[str] = Query(),
	role_service=DepRBACService,
	app_module_service=DepAppModuleService,
):
	print(role_service)
	modules = await app_module_service.get_modules_by_token_name(token_modules)
	roles = await role_service.get_all_roles_from_modules(modules)
	users = await user_service.get_all_user_with_roles([role.id for role in roles])
	return users
	# return await user_service.get_user_list(int(limit), int(page))


@user_router.get("/{user_id}")
@inject
async def get_user(
	user_service: DepUserService,
	user_uuid: uuid.UUID,
):
	return await user_service.get_user_by_uuid(str(user_uuid))


@user_router.post("")
async def create_user(
	user_service: DepUserService,
	request: CreateUserRequest,
):
	command = CreateUserCommand.model_validate(request.model_dump())
	return await user_service.create_user(command=command)


@user_router.put("/{user_uuid}/role")
@inject
async def asign_role(
	user_service: DepUserService,
	user_uuid: uuid.UUID,
	role: RoleRequest,
):
	return await user_service.asign_role_to_user(str(user_uuid), role.id)
