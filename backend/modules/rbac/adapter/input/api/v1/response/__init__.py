

from typing import List
from pydantic import BaseModel

from modules.module.domain.entity.module import Module
from modules.rbac.domain.entity import GroupPermission, Permission

class RoleResponse(BaseModel):
	id: int | None = None
	name: str | None = None
	description : str | None = None
	groups : List[GroupPermission] | None = []
	permissions : List[Permission] | None = []
	modules: List[Module] | None = []

class GroupResponse(BaseModel):
	id: int | None = None
	name: str | None = None
	description : str | None = None
	permissions : List[Permission] | None = []


class RoleAddPermissionResponse(BaseModel):
	id: int | None = None
	name: str
	permissions : List[Permission] | None = []

class RoleAddGroupsResponse(BaseModel):
	id: int | None = None
	name: str
	groups : List[GroupPermission] | None = []

class RoleAddModulesResponse(BaseModel):
	id: int | None = None
	name: str
	modules : List[Module] | None = []

class GroupAddPermissionResponse(BaseModel):
	id: int | None = None
	name: str
	permissions : List[Permission] | None = []

PermissionListResponse = List[Permission]