from pydantic import BaseModel, Field


class CreatePermissionRequest(BaseModel):
	name: str = Field(..., description="Name of permission")
	token: str = Field(..., description="Unique token of permission")
	description: str | None = Field(None,description="Description of permission")

class CreateRoleRequest(BaseModel):
	name: str = Field(..., description="Name of role")
	description: str | None = Field(None,description="Description of role")

class CreateGroupRequest(BaseModel):
	name: str = Field(..., description="Name of group")
	description: str | None = Field(None,description="Description of group")