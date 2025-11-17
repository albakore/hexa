from typing import List
import uuid
from pydantic import BaseModel, Field

from modules.module.application.dto import ModuleViewDTO


class GetUserListResponseDTO(BaseModel):
	id: uuid.UUID = Field(..., description="ID")
	email: str = Field(..., description="Email")
	nickname: str = Field(..., description="Nickname")
	is_admin: bool | None = Field(default=False, description="Set as admin")
	is_owner: bool | None = Field(default=False, description="Set as super admin")


class CreateUserRequestDTO(BaseModel):
	email: str = Field(..., description="Email")
	nickname: str | None = Field(default=None, description="Nickname")
	name: str | None = Field(default=None, description="Name")
	lastname: str | None = Field(default=None, description="Lastname")
	job_position: str | None = Field(default=None, description="Job Position")
	phone_number: str | None = Field(default=None, description="Phone Number")
	is_admin: bool = Field(default=False, description="Set as admin")
	is_owner: bool = Field(default=False, description="Set as super admin")


class CreateUserResponseDTO(BaseModel):
	email: str = Field(..., description="Email")
	nickname: str = Field(..., description="Nickname")


class UserLoginResponseDTO(BaseModel):
	id: uuid.UUID
	nickname: str | None = None
	email: str | None = None
	name: str | None = None
	lastname: str | None = None
	job_position: str | None = None
	fk_role: int | None = None
	is_admin: bool
	is_owner: bool


class LoginResponseDTO(BaseModel):
	user: UserLoginResponseDTO
	permissions: List[str]
	modules: List[ModuleViewDTO]
	token: str = Field(..., description="Token")
	refresh_token: str = Field(..., description="Refresh token")
