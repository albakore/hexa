from pydantic import BaseModel, Field


class CreateUserCommand(BaseModel):
	name: str
	lastname : str
	email: str
	nickname: str | None = Field(default=None)