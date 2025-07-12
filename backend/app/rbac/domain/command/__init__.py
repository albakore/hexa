from pydantic import BaseModel


class CreateRoleCommand(BaseModel):
	name: str
	description: str | None = None

class CreateGroupCommand(BaseModel):
	name: str
	description: str | None = None

class CreatePermissionCommand(BaseModel):
	name: str
	token: str
	description: str | None = None
