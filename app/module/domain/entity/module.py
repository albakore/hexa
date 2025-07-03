from typing import TYPE_CHECKING, List
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
	from app.rbac.domain.entity import Role

class ModuleRoleLink(SQLModel, table=True):
	fk_module : int = Field(primary_key=True, foreign_key='module.id')
	fk_role : int = Field(primary_key=True, foreign_key='role.id')

class Module(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	name : str
	token : str
	description : str | None = Field(default=None)

	roles : List['Role'] = Relationship(back_populates='modules', link_model=ModuleRoleLink)