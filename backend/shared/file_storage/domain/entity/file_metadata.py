from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
class FileMetadata(SQLModel, table=True):
	id : uuid.UUID = Field(default=None, primary_key=True)
	path_target : Optional[str] = Field(default=None)
	filename : str = Field(default=None)
	download_filename : Optional[str] = Field(default=None)
	size : Optional[int] = Field(default=None)

	date_created : Optional[datetime] = Field(default_factory=datetime.now)