from typing import Annotated
from dependency_injector.wiring import Provide, inject, provided
from fastapi import APIRouter, Depends

from app.container import MainContainer
from app.rbac.domain.command import CreateRoleCommand
from app.rbac.domain.usecase import RoleUseCase


rbac_router = APIRouter()

RoleUseCaseDependency = Annotated[RoleUseCase,Depends(Provide[MainContainer.rbac.role_service])]

@rbac_router.get("/role")
@inject
async def get_all_roles(
	role_usecase: RoleUseCaseDependency
):
	return await role_usecase.get_all_roles()


@rbac_router.get("/role/{id_role}")
async def get_role(id_role: int): ...


@rbac_router.post("/role")
@inject
async def create_role(
	command: CreateRoleCommand,
	role_usecase : RoleUseCaseDependency
):
	role = await role_usecase.create_role(command)
	new_role = await role_usecase.save(role)
	return new_role


@rbac_router.put("/role")
async def edit_role(): ...


@rbac_router.delete("/role/{id_role}")
async def delete_role(id_role: int): ...


@rbac_router.get("/permission")
async def get_all_permissions(): ...


@rbac_router.get("/permission/{id_permission}")
async def get_permission(id_permission: int): ...


@rbac_router.post("/permission")
async def create_permission(permission): ...


@rbac_router.put("/permission")
async def edit_permission(permission): ...


@rbac_router.delete("/permission/{id_permission}")
async def delete_permission(id_permission: int): ...
