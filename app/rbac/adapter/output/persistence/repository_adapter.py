from typing import List
from app.rbac.domain.entity import GroupPermission, Role, Permission
from app.rbac.domain.repository import PermissionRepository, RoleRepository


class RBACRepositoryAdapter(RoleRepository, PermissionRepository):
	def __init__(
		self,
		role_repository: RoleRepository,
		permission_repository: PermissionRepository,
	):
		self.role_repository = role_repository
		self.permission_repository = permission_repository

	async def get_all_permissions(self) -> List[Permission]:
		return await self.permission_repository.get_all_permissions()

	async def get_permission_by_id(self, id_permission: int) -> Permission | None:
		return await self.permission_repository.get_permission_by_id(id_permission)

	async def modify_permission(self, permission: Permission) -> Permission | None:
		return await self.permission_repository.modify_permission(permission)

	async def link_permission_to_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		return await self.permission_repository.link_permission_to_group(
			id_permission, id_group
		)

	async def unlink_permission_from_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		return await self.permission_repository.unlink_permission_from_group(
			id_permission, id_group
		)

	async def link_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		return await self.permission_repository.link_list_permissions_to_group(
			id_group, list_id_permission
		)

	async def unlink_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		return await self.permission_repository.unlink_list_permissions_to_group(
			id_group, list_id_permission
		)

	# async def delete(self, id_role: int) -> None:
	# 	return await self.role

	# async def save(self, role: Role) -> None:
	# 	raise NotImplementedError

	async def get_all_roles(self) -> List[Role]:
		return await self.role_repository.get_all_roles()

	async def get_role_by_id(self, id_role: int) -> Role | None:
		return await self.role_repository.get_role_by_id(id_role)

	async def modify_role(self, role: Role) -> Role | None:
		return await self.role_repository.modify_role(role)

	async def link_group_to_role(self, id_role: int, id_group: int) -> Role | None:
		return await self.role_repository.link_group_to_role(id_role, id_group)

	async def unlink_group_from_role(self, id_role: int, id_group: int) -> Role | None:
		return await self.role_repository.unlink_group_from_role(id_role, id_group)

	async def link_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		return await self.role_repository.link_grouplist_to_role(id_role, list_id_group)

	async def unlink_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		return await self.role_repository.unlink_grouplist_to_role(
			id_role, list_id_group
		)

	async def get_all_permissions_from_role(
		self, role: Role
	) -> List[Permission] | None:
		return await self.permission_repository.get_all_permissions_from_role(role)

	async def delete_permission(self, id_permission: int) -> None:
		return await self.permission_repository.delete_permission(id_permission)

	async def save_permission(self, permission: Permission) -> None:
		return await self.permission_repository.save_permission(permission)

	async def delete_role(self, id_role: int) -> None:
		return await self.role_repository.delete_role(id_role)

	async def save_role(self, role: Role) -> None:
		return await self.role_repository.save_role(role)
