from abc import ABC, abstractmethod
from typing import List

from app.rbac.domain.entity import Permission, Role
from app.rbac.domain.entity import GroupPermission


class PermissionRepository(ABC):
	@abstractmethod
	async def get_all_permissions(self) -> List[Permission]: ...

	@abstractmethod
	async def get_permission_by_id(self, id_permission: int) -> Permission | None: ...

	@abstractmethod
	async def get_permissions_by_ids(self, ids: list[int]) -> List[Permission]: ...

	@abstractmethod
	async def get_all_permissions_from_role(
		self, role: Role
	) -> List[Permission] | None: ...

	@abstractmethod
	async def link_permission_to_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None: ...

	@abstractmethod
	async def unlink_permission_from_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None: ...

	@abstractmethod
	async def link_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None: ...

	@abstractmethod
	async def unlink_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None: ...

	@abstractmethod
	async def delete_permission(self, permission: Permission) -> None: ...

	@abstractmethod
	async def save_permission(self, permission: Permission) -> None: ...

	@abstractmethod
	async def find_permissions(
		self, permissions: List[Permission]
	) -> List[Permission] | None: ...
