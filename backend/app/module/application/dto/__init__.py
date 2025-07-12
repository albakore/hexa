
from pydantic import BaseModel


class ModuleViewDTO(BaseModel):
	name: str
	token: str
	description : str