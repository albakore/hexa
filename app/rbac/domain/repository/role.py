from abc import ABC, abstractmethod
from typing import List

from app.rbac.domain.entity.permission import Permission
from app.rbac.domain.entity.role import Role


class RoleRepository(ABC):
	@abstractmethod
	async def get_all_roles(self) -> List[Role]: ...

	@abstractmethod
	async def get_role_by_id(self, id_role: int) -> Role | None: ...

	@abstractmethod
	async def link_group_to_role(self, id_role: int, id_group: int) -> Role | None: ...

	@abstractmethod
	async def unlink_group_from_role(
		self, id_role: int, id_group: int
	) -> Role | None: ...

	@abstractmethod
	async def link_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None: ...

	@abstractmethod
	async def unlink_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None: ...

	@abstractmethod
	def append_permission_to_role(
		self, permission: Permission, role: Role
	) -> Role | None: ...

	@abstractmethod
	async def delete_role(self, role: Role) -> None: ...

	@abstractmethod
	async def save_role(self, role: Role) -> None: ...
