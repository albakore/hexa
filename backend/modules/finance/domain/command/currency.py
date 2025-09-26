from pydantic import BaseModel


class CreateCurrencyCommand(BaseModel):
	id: int | None = None
	name: str
	code: str
	country: str | None = None


class UpdateCurrencyCommand(BaseModel):
	id: int
	name: str
	code: str
	country: str | None = None
