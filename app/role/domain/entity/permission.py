
from typing import List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
	from app.role.domain.entity.role import RoleGroupPermissionLink, Role
    

class GroupPermissionLink(SQLModel):
    fk_group: int = Field(foreign_key="grouppermission.id", primary_key=True)
    fk_permission: int = Field(foreign_key="permission.id", primary_key=True)


class GroupPermission(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = Field(default=None)

    permissions: List['Permission'] = Relationship(
        back_populates="groups", link_model=GroupPermissionLink
    )
    roles: List["Role"] = Relationship(
        back_populates="groups", link_model=RoleGroupPermissionLink
    )


class Permission(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    clave: str
    description: str | None = Field(default=None)

    groups: List["GroupPermission"] = Relationship(
        back_populates="permissions", link_model=GroupPermissionLink
    )