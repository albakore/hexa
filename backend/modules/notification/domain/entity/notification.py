import uuid
from sqlmodel import SQLModel, Field


class Notification(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	user_id: uuid.UUID | None = Field(default=None)
	name: str | None = Field(default=None)
	type: str | None = Field(default=None)
	message: str | None = Field(default=None)
	date_sent: str | None = Field(default=None)
	active: bool = True
