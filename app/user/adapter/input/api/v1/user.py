from typing import Annotated
import uuid
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Cookie, Depends, Query, WebSocket, WebSocketException,status

from app.user.adapter.input.api.v1.request import CreateUserRequest, RoleRequest
from app.user.application.service.user import UserService
from app.container import SystemContainer
from app.user.domain.command import CreateUserCommand

from core.fastapi.dependencies import PermissionDependency
from core.fastapi.dependencies.user_permission.user import UserTokenPermission

user_router = APIRouter()

@user_router.get(
	"",
	# dependencies=[UserTokenPermission.read]
)
@inject
# @TokenRegistry.register("user:read")
async def get_user_list(
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	user_service: UserService = Depends(Provide[SystemContainer.user.service]),
):
	return await user_service.get_user_list(int(limit),int(page))

@user_router.get("/{user_id}")
@inject
async def get_user(
	user_uuid: uuid.UUID,
	user_service: UserService = Depends(Provide[SystemContainer.user.service])
):
	return await user_service.get_user_by_uuid(str(user_uuid))


@user_router.post("")
@inject
async def create_user(
	request : CreateUserRequest,
	user_service: UserService = Depends(Provide[SystemContainer.user.service])
):
	command = CreateUserCommand.model_validate(request.model_dump())
	return await user_service.create_user(command=command)


@user_router.put("/{user_uuid}/role")
@inject
async def asign_role(
	user_uuid: uuid.UUID,
	role : RoleRequest,
	user_service: UserService = Depends(Provide[SystemContainer.user.service])
):
	return await user_service.asign_role_to_user(str(user_uuid), role.id)
