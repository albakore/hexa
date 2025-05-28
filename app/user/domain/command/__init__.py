from pydantic import BaseModel


class CreateUserCommand(BaseModel):
	name: str
	lastname : str
	email: str