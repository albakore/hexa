

from typing import List
from pydantic import BaseModel

from app.rbac.domain.entity import Permission


class RoleAddPermissionResponse(BaseModel):
	id: int | None = None
	name: str
	permissions : List[Permission] | None = []