import uuid
from sqlmodel import Field, SQLModel
from datetime import datetime

from core.helpers.password import PasswordHelper

class User(SQLModel, table=True):
	id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
	nickname: str | None = Field(default=None)
	name: str | None = Field(default=None)
	lastname: str | None = Field(default=None)
	job_position: str | None = Field(default=None)
	phone_number: str | None = Field(default=None)
	email: str
	password: str | None = Field(default=None)
	is_active: bool = Field(default=True)
	requires_password_reset: bool = Field(default=True)
	initial_password: str | None = Field(nullable=True, default_factory=PasswordHelper.generate_password)
	date_last_session: datetime = Field(default_factory=datetime.now)
	date_registration: datetime = Field(default_factory=datetime.now)
	fk_role: int | None = Field(default=None, foreign_key="role.id")
