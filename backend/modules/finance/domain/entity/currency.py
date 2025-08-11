from sqlmodel import SQLModel, Field

class Currency(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	name: str
	code: str
	symbol: str | None = Field(default=None)
	country: str | None = Field(default=None)