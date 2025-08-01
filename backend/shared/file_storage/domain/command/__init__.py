from typing import Any, BinaryIO, Optional
import uuid
from pydantic import BaseModel, field_validator

class SaveFileCommand(BaseModel):
	file: Any #BinaryIO
	path_target: Optional[str] = None
	filename: str
	download_filename : Optional[str] = None
	size:  Optional[int] = None

	@field_validator("path_target",mode="before")
	@classmethod
	def check_first_slash_character(cls, value: str):
		if len(value) == 1 and value == "/":
			return value

		if not '/' == value[0]:
			raise ValueError("First character must be '/'")
		
		if '/' == value[-1]:
			raise ValueError("Last character must not be '/'")

		return value

	model_config = {
        "arbitrary_types_allowed": True
    }

class CreateFileMetadataCommand(BaseModel):
	id: uuid.UUID
	path_target: str
	filename: str
	download_filename : Optional[str] = None
	size:  Optional[int] = None