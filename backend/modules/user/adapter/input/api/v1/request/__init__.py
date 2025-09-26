from pydantic import BaseModel, Field
from faker import Faker

faker = Faker()


class RoleRequest(BaseModel):
	id: int
	name: str


class CreateUserRequest(BaseModel):
	name: str = Field(default=faker.name())
	lastname: str = Field(default=faker.last_name())
	email: str = Field(default=faker.email())
