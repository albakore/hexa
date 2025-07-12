from pydantic import BaseModel, Field

class CreateProviderCommand(BaseModel):
	name : str = Field(...,description="Name of provider")