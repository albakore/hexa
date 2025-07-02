from sqlmodel import SQLModel, Field

class Module(SQLModel, table=True):
	id: int | None = Field(default=None, primary_key=True)
	name : str
	token : str
	description : str | None = Field(None)