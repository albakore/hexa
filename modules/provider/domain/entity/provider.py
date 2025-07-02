from sqlmodel import SQLModel, Relationship, Field

class Provider(SQLModel, table=True):
	id : int | None = Field(None, primary_key=True)
	name : str

	id_yiqi_provider : int | None = Field(None) 