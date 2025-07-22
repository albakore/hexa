from typing import TYPE_CHECKING, List
import uuid
from sqlmodel import SQLModel, Relationship, Field


if TYPE_CHECKING:
	from app.user.domain.entity.user import User
	

class UserProviderLink(SQLModel, table=True):
	fk_user : uuid.UUID | None = Field(default=None, primary_key=True, foreign_key='user.id')
	fk_provider : int | None = Field(default=None, primary_key=True, foreign_key='provider.id')

class Provider(SQLModel, table=True):
	id : int | None = Field(None, primary_key=True)
	name : str

	id_yiqi_provider : int | None = Field(None) 

	users: List["User"] = Relationship(back_populates='providers', link_model=UserProviderLink)