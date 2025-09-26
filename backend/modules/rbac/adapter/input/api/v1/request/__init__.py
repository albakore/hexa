from typing import List
from pydantic import BaseModel, Field

from modules.app_module.domain.entity.module import Module
from modules.rbac.domain.entity import GroupPermission, Permission


class CreatePermissionRequest(BaseModel):
	name: str = Field(..., description="Name of permission")
	token: str = Field(..., description="Unique token of permission")
	description: str | None = Field(None, description="Description of permission")


class CreateRoleRequest(BaseModel):
	name: str = Field(..., description="Name of role")
	description: str | None = Field(None, description="Description of role")


class UpdateRoleRequest(CreateRoleRequest): ...


class CreateGroupRequest(BaseModel):
	name: str = Field(..., description="Name of group")
	description: str | None = Field(None, description="Description of group")


class DeleteGroupRequest(BaseModel):
	id: int
	name: str = Field(..., description="Name of group")


AddPermissionToRoleRequest = List[Permission]

AddPermissionToGroupRequest = List[Permission]

AddGroupToRoleRequest = List[GroupPermission]

AddModuleToRoleRequest = List[Module]

RemovePermissionToRoleRequest = List[Permission]

RemoveGroupToRoleRequest = List[GroupPermission]

RemoveModulesToRoleRequest = List[Module]
