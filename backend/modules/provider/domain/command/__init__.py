from pydantic import BaseModel, Field

class CreateProviderCommand(BaseModel):
	name : str = Field(...,description="Name of provider")
	id_yiqi_provider : int | None = Field(default=None,description="Id of yiqi provider")

class UpdateProviderCommand(BaseModel):
	id : int
	name : str = Field(...,description="Name of provider")
	id_yiqi_provider : int | None = Field(default=None,description="Id of yiqi provider")