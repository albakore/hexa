from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.user.application.service.user import UserService
from app.container import MainContainer

user_router = APIRouter()

@user_router.get("")
@inject
def get_user_list(
	user_service: UserService = Depends(Provide[MainContainer.user.service])
):
	return user_service.get_user_list()