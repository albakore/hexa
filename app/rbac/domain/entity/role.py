from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
	from app.rbac.domain.entity import GroupPermission, Permission
	from app.user.domain.entity import User

class RoleGroupPermissionLink(SQLModel, table=True):
	fk_role: int = Field(foreign_key="role.id", primary_key=True)
	fk_group: int = Field(foreign_key="grouppermission.id", primary_key=True)


class RolePermissionLink(SQLModel, table=True):
	fk_role: int = Field(foreign_key="role.id", primary_key=True)
	fk_permission: int = Field(foreign_key="permission.id", primary_key=True)


class Role(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	name: str
	description: str | None = Field(default=None)

	groups: List["GroupPermission"] = Relationship(
		back_populates="roles", link_model=RoleGroupPermissionLink
	)

	permissions: List["Permission"] = Relationship(
		back_populates="roles", link_model=RolePermissionLink
	)

	users: List["User"] = Relationship(back_populates="role")
