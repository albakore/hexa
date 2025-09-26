from typing import List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


from modules.rbac.domain.entity.role import (
	RoleGroupPermissionLink,
	Role,
	RolePermissionLink,
)


class GroupPermissionLink(SQLModel, table=True):
	fk_group: int = Field(foreign_key="grouppermission.id", primary_key=True)
	fk_permission: int = Field(foreign_key="permission.id", primary_key=True)


class GroupPermission(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	name: str
	description: str | None = Field(default=None)

	permissions: List["Permission"] = Relationship(
		back_populates="groups", link_model=GroupPermissionLink
	)
	roles: List["Role"] = Relationship(
		back_populates="groups", link_model=RoleGroupPermissionLink
	)


class Permission(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	group_name: str | None = Field(default=None)
	name: str
	token: str
	description: str | None = Field(default=None)

	groups: List["GroupPermission"] = Relationship(
		back_populates="permissions", link_model=GroupPermissionLink
	)

	roles: List["Role"] = Relationship(
		back_populates="permissions", link_model=RolePermissionLink
	)
