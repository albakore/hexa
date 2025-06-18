from typing import List
from app.rbac.application.exception import GroupNotFoundException, RoleNotFoundException
from app.rbac.domain.command import CreateGroupCommand, CreatePermissionCommand
from app.rbac.domain.entity import Permission, Role
from app.rbac.domain.entity import GroupPermission
from app.rbac.domain.repository import PermissionRepository
from app.rbac.domain.usecase import PermissionUseCase
from core.db import Transactional


class PermissionService(PermissionUseCase):
	def __init__(self, permission_repository: PermissionRepository):
		self.permission_repository = permission_repository

	async def get_all_permissions(self) -> List[Permission]:
		return await self.permission_repository.get_all_permissions()

	async def get_permission_by_id(self, id_permission: int) -> Permission | None:
		return await self.permission_repository.get_permission_by_id(id_permission)

	@Transactional()
	async def delete(self, permission: Permission) -> None:
		return await self.permission_repository.delete_permission(permission)

	@Transactional()
	async def save(self, permission: Permission) -> None:
		return await self.permission_repository.save_permission(permission)

	async def get_all_permissions_from_role(self, role: Role) -> List[str]:
		permissions = await self.permission_repository.get_all_permissions_from_role(
			role
		)
		return permissions

	async def modify_permission(self, permission: Permission) -> Permission | None:
		raise NotImplementedError

	def create_permission(self, command: CreatePermissionCommand) -> Permission:
		permission = Permission.model_validate(command)
		return permission

	async def find_permissions(
		self, permissions: List[Permission]
	) -> List[Permission] | None:
		return await self.permission_repository.find_permissions(permissions)

	def create_group(self, command: CreateGroupCommand) -> GroupPermission:
		group = GroupPermission.model_validate(command)
		return group

	async def append_permissions_to_group(
		self, permissions: List[Permission], id_group: int
	) -> GroupPermission:
		group = await self.permission_repository.get_group_by_id(
			id_group, with_permissions=True
		)
		if not group:
			raise GroupNotFoundException

		permission_ids = [p.id for p in permissions]

		permissions_from_db = await self.permission_repository.get_permissions_by_ids(
			permission_ids  # type:ignore
		)

		for permission in permissions_from_db:
			if permission not in group.permissions:
				group.permissions.append(permission)

		return await self.permission_repository.save_group(group)

	async def get_all_groups(self) -> List[GroupPermission]:
		return await self.permission_repository.get_all_groups()

	async def get_group_by_id(
		self, id_group: int, with_permissions: bool = False, with_roles: bool = False
	) -> GroupPermission:
		group =  await self.permission_repository.get_group_by_id(
			id_group,
			with_permissions,
			with_roles
		)
		if not group:
			raise GroupNotFoundException
		return group

	@Transactional()
	async def save_group(self, group: GroupPermission) -> GroupPermission:
		return await self.permission_repository.save_group(group)

	@Transactional()
	async def delete_group(self, group: GroupPermission) -> None:
		return await self.permission_repository.delete_group(group)
