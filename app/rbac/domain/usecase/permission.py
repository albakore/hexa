from abc import ABC, abstractmethod
from typing import List
from app.rbac.domain.command import CreatePermissionCommand
from app.rbac.domain.entity import Permission, Role
from app.rbac.domain.entity import GroupPermission


class PermissionUseCase(ABC):
	
	@abstractmethod
	async def get_all_permissions(self) -> List[Permission]:
		raise NotImplementedError

	@abstractmethod
	async def get_permission_by_id(self, id_permission: int) -> Permission | None:
		raise NotImplementedError
	
	@abstractmethod
	async def find_permissions(self, permissions: List[Permission]) -> List[Permission] | None:
		raise NotImplementedError

	@abstractmethod
	async def get_all_permissions_from_role(self, role: Role) -> List[str] | None:
		raise NotImplementedError

	@abstractmethod
	async def modify_permission(self, permission: Permission) -> Permission | None:
		raise NotImplementedError

	@abstractmethod
	async def link_permission_to_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		raise NotImplementedError

	@abstractmethod
	async def unlink_permission_from_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		raise NotImplementedError

	@abstractmethod
	async def link_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		raise NotImplementedError

	@abstractmethod
	async def unlink_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		raise NotImplementedError

	@abstractmethod
	async def delete(self, permission: Permission) -> None:
		raise NotImplementedError

	@abstractmethod
	async def save(self, permission: Permission) -> None:
		raise NotImplementedError

	@abstractmethod
	def create_permission(self, command: CreatePermissionCommand) -> Permission:
		raise NotImplementedError
