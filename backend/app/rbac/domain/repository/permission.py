from abc import ABC, abstractmethod
from typing import List, Sequence

from app.rbac.domain.entity import Permission, Role
from app.rbac.domain.entity import GroupPermission


class PermissionRepository(ABC):
	@abstractmethod
	async def get_all_permissions(self) -> List[Permission]: ...

	@abstractmethod
	async def get_permission_by_id(self, id_permission: int) -> Permission | None: ...

	@abstractmethod
	async def get_permissions_by_ids(
		self, ids: list[int]
	) -> List[Permission] | Sequence[Permission]: ...

	@abstractmethod
	async def get_all_permissions_from_role(
		self, role: Role
	) -> List[Permission] | Sequence[Permission]: ...

	@abstractmethod
	async def delete_permission(self, permission: Permission) -> None: ...

	@abstractmethod
	async def save_permission(self, permission: Permission) -> None: ...

	@abstractmethod
	async def find_permissions(
		self, permissions: List[Permission]
	) -> List[Permission] | Sequence[Permission]: ...

	@abstractmethod
	async def get_all_groups(
		self,
	) -> List[GroupPermission] | Sequence[GroupPermission]: ...

	@abstractmethod
	async def get_group_by_id(
		self,
		id_group: int,
		with_permissions: bool = False,
		with_roles: bool = False,
	) -> GroupPermission | None: ...

	@abstractmethod
	async def get_groups_by_ids(
		self, ids: List[int]
	) -> List[GroupPermission] | Sequence[GroupPermission]: ...

	@abstractmethod
	async def save_group(self, group: GroupPermission) -> GroupPermission: ...

	@abstractmethod
	async def delete_group(self, group: GroupPermission) -> None: ...
