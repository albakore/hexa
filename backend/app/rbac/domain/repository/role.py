from abc import ABC, abstractmethod
from typing import List, Sequence

from app.module.domain.entity.module import Module
from app.rbac.domain.entity import GroupPermission
from app.rbac.domain.entity.permission import Permission
from app.rbac.domain.entity.role import Role


class RoleRepository(ABC):
	@abstractmethod
	async def get_all_roles(self) -> List[Role] | Sequence[Role]: ...

	@abstractmethod
	async def get_role_by_id(
		self,
		id_role: int,
		with_permissions: bool = False,
		with_groups: bool = False,
		with_modules: bool = False,
	) -> Role | None: ...

	@abstractmethod
	async def append_permissions_to_role(
		self, permissions: List[Permission], id_role: int
	) -> Role: ...

	@abstractmethod
	async def remove_permissions_to_role(
		self, permissions: List[Permission], id_role: int
	) -> int: ...

	@abstractmethod
	async def remove_group_permissions_to_role(
		self, groups: List[GroupPermission], id_role: int
	) -> int: ...

	@abstractmethod
	async def append_modules_to_role(
		self, modules: List[Module], id_role: int
	) -> Role: ...

	@abstractmethod
	async def remove_modules_to_role(self, modules: List[int], id_role: int) -> int: ...

	@abstractmethod
	async def delete_role(self, role: Role) -> Role | None: ...

	@abstractmethod
	async def save_role(self, role: Role) -> Role: ...

	@abstractmethod
	async def get_all_modules_from_role(
		self, role: Role
	) -> List[Module] | Sequence[Module]: ...

	@abstractmethod
	async def get_all_roles_from_modules(
		self, modules_ids: List[int]
	) -> List[Role] | Sequence[Role]: ...
