from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class YiqiEntity(BaseModel):
	id : Optional[int] = Field(default=None)

	__internal_name__ : str = "ENTITY"
	"""Variable utilizada para conocer como es llamada la entidad en yiqi"""
	
	__prefix__ : str = ""

	@classmethod
	def alias_generator(cls, field_name: str) -> str:
		if "_ID_" or "id" in field_name:
			return field_name
		return f"{cls.__prefix__}_{field_name}"

	model_config = ConfigDict(
		alias_generator=lambda field_name: field_name,  # placeholder
		populate_by_name=True,
		
	)

	def __init_subclass__(cls, **kwargs):
		cls.model_config = ConfigDict(
			alias_generator=cls.alias_generator,
			populate_by_name=True
		)

	@classmethod
	def get_attributes(cls):
		return [field.alias for field in cls.model_fields.values()]


