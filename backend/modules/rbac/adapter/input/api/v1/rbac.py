from fastapi import APIRouter, Depends, Query
from shared.dependencies import get_role_service, get_permission_service
from dependency_injector.wiring import Provide, inject

rbac_router = APIRouter()


@rbac_router.get("/roles")
async def get_all_roles(role_service=Depends(get_role_service)):
	return await role_service.get_all_roles()


@rbac_router.post("/roles")
async def create_role(request: dict, role_service=Depends(get_role_service)):
	return await role_service.create_role(request)


@rbac_router.get("/roles/{role_id}")
async def get_role(role_id: int, role_service=Depends(get_role_service)):
	return await role_service.get_role_by_id(role_id)


@rbac_router.put("/roles/{role_id}")
async def update_role(
	role_id: int, request: dict, role_service=Depends(get_role_service)
):
	return await role_service.update_role(role_id, request)


@rbac_router.delete("/roles/{role_id}")
async def delete_role(role_id: int, role_service=Depends(get_role_service)):
	return await role_service.delete_role(role_id)


@rbac_router.get("/permissions")
@inject
async def get_all_permissions(
	permission_service=Depends(Provide[get_permission_service]),
):
	return await permission_service.get_all_permissions()


@rbac_router.post("/permissions")
async def create_permission(
	request: dict, permission_service=Depends(get_permission_service)
):
	return await permission_service.create_permission(request)


@rbac_router.get("/permissions/{permission_id}")
async def get_permission(
	permission_id: int, permission_service=Depends(get_permission_service)
):
	return await permission_service.get_permission_by_id(permission_id)


@rbac_router.put("/permissions/{permission_id}")
async def update_permission(
	permission_id: int,
	request: dict,
	permission_service=Depends(get_permission_service),
):
	return await permission_service.update_permission(permission_id, request)


@rbac_router.delete("/permissions/{permission_id}")
async def delete_permission(
	permission_id: int, permission_service=Depends(get_permission_service)
):
	return await permission_service.delete_permission(permission_id)


@rbac_router.post("/users/{user_id}/roles/{role_id}")
async def assign_role_to_user(
	user_id: int, role_id: int, role_service=Depends(get_role_service)
):
	return await role_service.assign_role_to_user(user_id, role_id)


@rbac_router.delete("/users/{user_id}/roles/{role_id}")
async def remove_role_from_user(
	user_id: int, role_id: int, role_service=Depends(get_role_service)
):
	return await role_service.remove_role_from_user(user_id, role_id)


@rbac_router.get("/users/{user_id}/roles")
async def get_user_roles(user_id: int, role_service=Depends(get_role_service)):
	return await role_service.get_user_roles(user_id)


@rbac_router.post("/permissions/check")
async def check_permission(
	request: dict, permission_service=Depends(get_permission_service)
):
	return await permission_service.check_permission(
		request.get("user_id"), request.get("resource"), request.get("action")
	)
