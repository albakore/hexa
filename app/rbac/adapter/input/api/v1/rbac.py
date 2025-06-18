from typing import Annotated
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.container import MainContainer
from app.rbac.adapter.input.api.v1.request import AddPermissionToRoleRequest, CreatePermissionRequest, CreateRoleRequest
from app.rbac.adapter.input.api.v1.response import RoleAddPermissionResponse, RoleResponse
from app.rbac.application.exception import PermissionNotFoundException, RoleNotFoundException
from app.rbac.domain.command import CreatePermissionCommand, CreateRoleCommand
from app.rbac.domain.usecase import PermissionUseCase, RoleUseCase


rbac_router = APIRouter()

RoleUseCaseDependency = Annotated[RoleUseCase,Depends(Provide[MainContainer.rbac.role_service])]
PermissionUseCaseDependency = Annotated[PermissionUseCase,Depends(Provide[MainContainer.rbac.permission_service])]


# region Role
# ______________ ROLE _________________

@rbac_router.get("/role")
@inject
async def get_all_roles(
	role_usecase: RoleUseCaseDependency
):
	return await role_usecase.get_all_roles()


@rbac_router.get(
	"/role/{id_role}",
	response_model=RoleResponse
)
@inject
async def get_role(
	id_role: int,
	role_usecase : RoleUseCaseDependency
	): 
	return await role_usecase.get_role_by_id(
		id_role,
		with_permissions=True,
		with_groups=True
	)



@rbac_router.post("/role")
@inject
async def create_role(
	command: CreateRoleRequest,
	role_usecase : RoleUseCaseDependency
):
	role_command = CreateRoleCommand.model_validate(command.model_dump())
	role = await role_usecase.create_role(role_command)
	return await role_usecase.save(role)


@rbac_router.put("/role")
async def edit_role(): ...


@rbac_router.put(
	"/role/{id_role}/add/permission",
	response_model=RoleAddPermissionResponse
)
@inject
async def add_permissions_to_role(
	id_role: int,
	permissions : AddPermissionToRoleRequest,
	role_usecase : RoleUseCaseDependency,
	permission_usecase : PermissionUseCaseDependency
):
	return await role_usecase.append_permissions_to_role(permissions,id_role)

@rbac_router.delete("/role/{id_role}")
@inject
async def delete_role(
	id_role: int,
	role_usecase : RoleUseCaseDependency,
	):
	await role_usecase.delete(id_role)
	return {'status': 'ok'}

# region Permission
# ______________ PERMISSION _________________


@rbac_router.get("/permission")
@inject
async def get_all_permissions(
	permission_usecase : PermissionUseCaseDependency
):
	return await permission_usecase.get_all_permissions()



@rbac_router.get("/permission/{id_permission}")
@inject
async def get_permission(
	id_permission: int,
	permission_usecase: PermissionUseCaseDependency

):
	...


@rbac_router.post("/permission")
@inject
async def create_permission(
	command: CreatePermissionRequest,
	permission_usecase : PermissionUseCaseDependency
):
	permission_command = CreatePermissionCommand.model_validate(command.model_dump())
	permission = permission_usecase.create_permission(permission_command)
	return await permission_usecase.save(permission)
	


@rbac_router.put("/permission")
async def edit_permission(permission): ...


@rbac_router.delete("/permission/{id_permission}")
async def delete_permission(id_permission: int): ...


# region Group
# ______________ GROUP _________________


@rbac_router.get("/group")
@inject
async def get_all_groups(
	permission_usecase: PermissionUseCaseDependency
):
	return await permission_usecase.get_all_groups()
