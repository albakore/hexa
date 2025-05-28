from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.user.adapter.input.api.v1.request import CreateUserRequest
from app.user.application.service.user import UserService
from app.container import MainContainer
from app.user.domain.command import CreateUserCommand

user_router = APIRouter()

@user_router.get("")
@inject
async def get_user_list(
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	user_service: UserService = Depends(Provide[MainContainer.user.service])
):
	return await user_service.get_user_list(int(limit),int(page))

@user_router.get("/{user_id}")
@inject
async def get_user(
	user_id: int,
	user_service: UserService = Depends(Provide[MainContainer.user.service])
):
	return await user_service.get_user_by_id(int(user_id))


@user_router.post("")
@inject
async def create_user(
	request : CreateUserRequest,
	user_service: UserService = Depends(Provide[MainContainer.user.service])
):
	command = CreateUserCommand.model_validate(request.model_dump())
	return await user_service.create_user(command=command)