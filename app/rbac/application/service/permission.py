from typing import List
from app.rbac.domain.entity.permission import Permission
from app.rbac.domain.entity.role import GroupPermission
from app.rbac.domain.usecase.permission import PermissionUseCase


class PermissionService(PermissionUseCase):
	def get_all_permissions(self) -> List[Permission]:
		raise NotImplementedError

	def get_permission_by_id(self, id_permission: int) -> Permission | None:
		raise NotImplementedError

	def modify_permission(self, permission: Permission) -> Permission | None:
		raise NotImplementedError

	def link_permission_to_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		raise NotImplementedError

	def unlink_permission_from_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		raise NotImplementedError

	def link_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		raise NotImplementedError

	def unlink_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		raise NotImplementedError

	def delete(self, id_permission: int) -> None:
		raise NotImplementedError

	def save(self, permission: Permission) -> None:
		raise NotImplementedError
