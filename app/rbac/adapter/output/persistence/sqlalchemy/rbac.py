from typing import List
from app.rbac.domain.entity.permission import Permission
from app.rbac.domain.entity import GroupPermission, Role
from app.rbac.domain.repository import RoleRepository, PermissionRepository


class RBACSQLAlchemyRepository(RoleRepository, PermissionRepository):
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

	def delete(self, id_role: int) -> None:
		raise NotImplementedError

	def save(self, role: Role) -> None:
		raise NotImplementedError

	def get_all_roles(self) -> List[Role]:
		raise NotImplementedError

	def get_role_by_id(self, id_role: int) -> Role | None:
		raise NotImplementedError

	def modify_role(self, role: Role) -> Role | None:
		raise NotImplementedError

	def link_group_to_role(self, id_role: int, id_group: int) -> Role | None:
		raise NotImplementedError

	def unlink_group_from_role(self, id_role: int, id_group: int) -> Role | None:
		raise NotImplementedError

	def link_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		raise NotImplementedError

	def unlink_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		raise NotImplementedError
