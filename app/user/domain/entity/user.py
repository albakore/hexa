from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel):
	id: int | None = Field(default=None, primary_key=True)
	name: str
	lastname: str
	job_position: str | None = Field(default=None)
	phone_number: str | None = Field(default=None)
	email: str
	is_active: bool = Field(default=True)
	date_last_session: datetime = Field(default_factory=datetime.now)
	date_registration: datetime = Field(default_factory=datetime.now)
	fk_role: int = Field(default=None, foreign_key="role.id")
