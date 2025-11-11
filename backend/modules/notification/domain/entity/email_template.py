from sqlalchemy import Column, LargeBinary
from sqlmodel import SQLModel, Field


class EmailTemplate(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	name: str | None = Field(default=None)
	description: str | None = Field(default=None)
	template_html: bytes | None = Field(default=None, sa_column=Column(LargeBinary))
	module: str | None = Field(
		default=None
	)  # módulo al que pertenece (usuarios, notificaciones, etc).
