import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Security

from core.fastapi.dependencies import require_permissions
from modules.user.adapter.input.api.v1.request import CreateUserRequest, RoleRequest
from modules.user.application.service.user import UserService
from modules.user.container import UserContainer
from modules.user.domain.command import CreateUserCommand
from shared.interfaces.service_locator import service_locator

user_router = APIRouter()


@user_router.get("")
@inject
async def get_user_list(
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	user_service: UserService = Depends(Provide[UserContainer.service]),
	_: None = Security(require_permissions("user:read")),
):
	"""
	Lista todos los usuarios con paginación.

	Requiere el permiso: user:read
	"""
	return await user_service.get_user_list(int(limit), int(page))


@user_router.get(
	"/search",
	# dependencies=[UserTokenPermission.read]
)
@inject
# @TokenRegistry.register("user:read")
async def search_users(
	token_modules: list[str] = Query(),
	role_service=Depends(service_locator.get_dependency("rbac.role_service")),
	app_module_service=Depends(service_locator.get_dependency("app_module_service")),
	user_service: UserService = Depends(Provide[UserContainer.service]),
):
	modules = await app_module_service.get_modules_by_token_name(token_modules)
	roles = await role_service.get_all_roles_from_modules(
		[module.id for module in modules]
	)
	users = await user_service.get_all_user_with_roles([role.id for role in roles])
	return users
	# return await user_service.get_user_list(int(limit), int(page))


@user_router.get("/{user_id}")
@inject
async def get_user(
	user_uuid: uuid.UUID,
	user_service: UserService = Depends(Provide[UserContainer.service]),
):
	return await user_service.get_user_by_uuid(str(user_uuid))


@user_router.post("")
@inject
async def create_user(
	request: CreateUserRequest,
	user_service: UserService = Depends(Provide[UserContainer.service]),
):
	command = CreateUserCommand.model_validate(request.model_dump())
	return await user_service.create_user(command=command)


@user_router.put("/{user_uuid}/role")
@inject
async def asign_role(
	user_uuid: uuid.UUID,
	role: RoleRequest,
	user_service: UserService = Depends(Provide[UserContainer.service]),
):
	return await user_service.asign_role_to_user(str(user_uuid), role.id)
