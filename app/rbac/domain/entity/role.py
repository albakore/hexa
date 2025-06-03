
from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.rbac.domain.entity.permission import GroupPermission

class RoleGroupPermissionLink(SQLModel, table=True):
    fk_role: int = Field(foreign_key="role.id", primary_key=True)
    fk_group: int = Field(foreign_key="grouppermission.id", primary_key=True)

class Role(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	name: str
	description: str | None = Field(default=None)

	groups : List['GroupPermission'] = Relationship(
		back_populates="roles", link_model=RoleGroupPermissionLink
	)
