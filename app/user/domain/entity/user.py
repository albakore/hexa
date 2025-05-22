from sqlmodel import Field, SQLModel

class User(SQLModel):
	id: int | None = Field(default=None, primary_key=True)
	nombre: str
	apellido: str