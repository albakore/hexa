from typing import List, Sequence
from modules.app_module.domain.entity.module import Module
from modules.rbac.domain.entity import GroupPermission, Role, Permission
from modules.rbac.domain.repository import (
	PermissionRepository,
	RBACRepository,
	RoleRepository,
)


class RBACRepositoryAdapter(RBACRepository):
	def __init__(
		self,
		role_repository: RoleRepository,
		permission_repository: PermissionRepository,
	):
		self.role_repository = role_repository
		self.permission_repository = permission_repository

	async def get_all_permissions(self) -> List[Permission] | Sequence[Permission]:
		return await self.permission_repository.get_all_permissions()

	async def get_permission_by_id(self, id_permission: int) -> Permission | None:
		return await self.permission_repository.get_permission_by_id(id_permission)

	async def get_all_roles(self) -> List[Role] | Sequence[Role]:
		return await self.role_repository.get_all_roles()

	async def get_role_by_id(
		self,
		id_role: int,
		with_permissions: bool = False,
		with_groups: bool = False,
		with_modules: bool = False,
	) -> Role | None:
		return await self.role_repository.get_role_by_id(
			id_role, with_permissions, with_groups, with_modules
		)

	async def get_permissions_by_ids(
		self, ids: list[int]
	) -> List[Permission] | Sequence[Permission]:
		return await self.permission_repository.get_permissions_by_ids(ids)

	async def get_all_permissions_from_role(
		self, role: Role
	) -> List[Permission] | Sequence[Permission]:
		return await self.permission_repository.get_all_permissions_from_role(role)

	async def delete_permission(self, permission: Permission) -> None:
		await self.permission_repository.delete_permission(permission)

	async def save_permission(self, permission: Permission) -> Permission | None:
		return await self.permission_repository.save_permission(permission)

	async def delete_role(self, role: Role) -> None:
		await self.role_repository.delete_role(role)

	async def save_role(self, role: Role) -> Role | None:
		return await self.role_repository.save_role(role)

	async def append_permissions_to_role(
		self, permissions: List[Permission], id_role: int
	) -> Role:
		return await self.role_repository.append_permissions_to_role(
			permissions, id_role
		)

	async def find_permissions(
		self, permissions: List[Permission]
	) -> List[Permission] | Sequence[Permission]:
		return await self.permission_repository.find_permissions(permissions)

	async def get_all_groups(self) -> List[GroupPermission] | Sequence[GroupPermission]:
		return await self.permission_repository.get_all_groups()

	async def get_group_by_id(
		self,
		id_group: int,
		with_permissions: bool = False,
		with_roles: bool = False,
	) -> GroupPermission | None:
		return await self.permission_repository.get_group_by_id(
			id_group, with_permissions, with_roles
		)

	async def get_groups_by_ids(
		self, ids: List[int]
	) -> List[GroupPermission] | Sequence[GroupPermission]:
		return await self.permission_repository.get_groups_by_ids(ids)

	async def save_group(self, group: GroupPermission) -> GroupPermission:
		return await self.permission_repository.save_group(group)

	async def delete_group(self, group: GroupPermission) -> None:
		return await self.permission_repository.delete_group(group)

	async def append_modules_to_role(
		self, modules_ids: List[int], id_role: int
	) -> Role:
		return await self.role_repository.append_modules_to_role(modules_ids, id_role)

	async def get_all_modules_from_role(
		self, role: Role
	) -> List[Module] | Sequence[Module]:
		return await self.role_repository.get_all_modules_from_role(role)

	async def remove_permissions_to_role(
		self, permissions: List[Permission], id_role: int
	) -> int:
		return await self.role_repository.remove_permissions_to_role(
			permissions, id_role
		)

	async def remove_group_permissions_to_role(
		self, groups: List[GroupPermission], id_role: int
	) -> int:
		return await self.role_repository.remove_group_permissions_to_role(
			groups, id_role
		)

	async def remove_modules_to_role(self, modules_ids: List[int], id_role: int) -> int:
		return await self.role_repository.remove_modules_to_role(modules_ids, id_role)

	async def get_all_roles_from_modules(
		self, modules_ids: List[int]
	) -> List[Role] | Sequence[Role]:
		return await self.role_repository.get_all_roles_from_modules(modules_ids)
