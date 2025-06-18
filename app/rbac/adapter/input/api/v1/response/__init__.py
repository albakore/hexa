

from typing import List
from pydantic import BaseModel

from app.rbac.domain.entity import GroupPermission, Permission

class RoleResponse(BaseModel):
	id: int | None = None
	name: str | None = None
	description : str | None = None
	groups : List[GroupPermission] | None = []
	permissions : List[Permission] | None = []

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

class GroupAddPermissionResponse(BaseModel):
	id: int | None = None
	name: str
	permissions : List[Permission] | None = []

PermissionListResponse = List[Permission]