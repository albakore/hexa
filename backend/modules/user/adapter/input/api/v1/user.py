from typing import Annotated, List
import uuid
from fastapi import (
	APIRouter,
	Cookie,
	Depends,
	Query,
	WebSocket,
	WebSocketException,
	status,
)
from shared.dependencies import get_user_service, get_role_service, get_app_module_service
from core.fastapi.dependencies import PermissionDependency
from core.fastapi.dependencies.user_permission.user import UserTokenPermission

user_router = APIRouter()


@user_router.get(
	"",
	# dependencies=[UserTokenPermission.read]
)
async def get_user_list(
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	user_service = Depends(get_user_service),
):
	return await user_service.get_user_list(int(limit), int(page))


@user_router.get(
	"/search",
	# dependencies=[UserTokenPermission.read]
)
async def search_users(
	token_modules: list[str] = Query(),
	user_service = Depends(get_user_service),
	role_service = Depends(get_role_service),
	app_module_service = Depends(get_app_module_service),
):
	modules = await app_module_service.get_modules_by_token_name(token_modules)
	roles = await role_service.get_all_roles_from_modules(modules)
	users = await user_service.get_all_user_with_roles([role.id for role in roles])
	return users


@user_router.get("/{user_id}")
async def get_user(
	user_uuid: uuid.UUID,
	user_service = Depends(get_user_service),
):
	return await user_service.get_user_by_uuid(str(user_uuid))


@user_router.post("")
async def create_user(
	request: dict,  # Simplified for now
	user_service = Depends(get_user_service),
):
	return await user_service.create_user(request)


@user_router.put("/{user_uuid}/role")
async def asign_role(
	user_uuid: uuid.UUID,
	role: dict,  # Simplified for now
	user_service = Depends(get_user_service),
):
	return await user_service.asign_role_to_user(str(user_uuid), role.get("id"))
