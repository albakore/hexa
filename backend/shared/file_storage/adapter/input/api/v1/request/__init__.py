from pydantic import BaseModel


# Temporalmente simplificado - las clases de comando serán redefinidas
class ProviderCreateRequest(BaseModel):
	name: str
	description: str = ""


class ProviderUpdateRequest(BaseModel):
	name: str = None
	description: str = None
