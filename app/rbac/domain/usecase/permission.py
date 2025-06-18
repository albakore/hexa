from abc import ABC, abstractmethod
from typing import List
from app.rbac.domain.command import CreateGroupCommand, CreatePermissionCommand
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
	async def delete(self, permission: Permission) -> None:
		raise NotImplementedError

	@abstractmethod
	async def save(self, permission: Permission) -> None:
		raise NotImplementedError

	@abstractmethod
	def create_permission(self, command: CreatePermissionCommand) -> Permission:
		raise NotImplementedError

	# region Group

	@abstractmethod
	async def get_all_groups(self) -> List[GroupPermission]:
		raise NotImplementedError
	
	@abstractmethod
	async def get_group_by_id(
		self,
		id_group : int,
		with_permissions : bool = False,	
		with_roles : bool = False,	
	) -> GroupPermission:
		raise NotImplementedError
	
	@abstractmethod
	def create_group(self, command: CreateGroupCommand) -> GroupPermission:
		raise NotImplementedError
	
	
	@abstractmethod
	async def save_group(self, group: GroupPermission) -> GroupPermission:
		raise NotImplementedError
	
	@abstractmethod
	async def append_permissions_to_group(
		self, permissions: List[Permission], id_group: int
	) -> GroupPermission:
		raise NotImplementedError