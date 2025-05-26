from abc import ABC, abstractmethod
from typing import List
from app.role.domain.entity.permission import Permission
from app.role.domain.entity.role import GroupPermission


class PermissionUseCase(ABC):

	@abstractmethod
	def get_all_permissions(self) -> List[Permission]:
		raise NotImplementedError

	@abstractmethod
	def get_permission_by_id(self, id_permission: int) -> Permission | None:
		raise NotImplementedError

	@abstractmethod
	def modify_permission(self, permission: Permission) -> Permission | None:
		raise NotImplementedError

	@abstractmethod
	def link_permission_to_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		raise NotImplementedError

	@abstractmethod
	def unlink_permission_from_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		raise NotImplementedError

	@abstractmethod
	def link_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		raise NotImplementedError

	@abstractmethod
	def unlink_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		raise NotImplementedError

	@abstractmethod
	def delete(self, id_permission: int) -> None:
		raise NotImplementedError

	@abstractmethod
	def save(self, permission: Permission) -> None:
		raise NotImplementedError
