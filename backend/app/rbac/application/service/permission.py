from typing import List
from app.rbac.application.exception import GroupNotFoundException, RoleNotFoundException
from app.rbac.domain.command import CreateGroupCommand, CreatePermissionCommand
from app.rbac.domain.entity import Permission, Role
from app.rbac.domain.entity import GroupPermission
from app.rbac.domain.repository import PermissionRepository
from app.rbac.domain.usecase.permission import PermissionUseCaseFactory
from core.db import Transactional
from dataclasses import dataclass


@dataclass
class PermissionService:
	permission_repository: PermissionRepository

	def __post_init__(self):
		self.permission_usecase = PermissionUseCaseFactory(
			self.permission_repository
		)

	async def get_all_permissions(self) -> List[Permission]:
		return await self.permission_usecase.get_all_permissions()

	async def get_permission_by_id(self, id_permission: int) -> Permission | None:
		return await self.permission_usecase.get_permission_by_id(id_permission)

	@Transactional()
	async def delete(self, permission: Permission) -> None:
		return await self.permission_usecase.delete_permission(permission)

	@Transactional()
	async def save(self, permission: Permission) -> None:
		return await self.permission_usecase.save_permission(permission)

	async def get_all_permissions_from_role(self, role: Role) -> List[str]:
		return await self.permission_usecase.get_all_permissions_from_role(role)

	async def modify_permission(self, permission: Permission) -> Permission | None:
		return await self.permission_usecase.modify_permission(permission)

	def create_permission(self, command: CreatePermissionCommand) -> Permission:
		return self.permission_usecase.create_permission(command)

	async def find_permissions(
		self, permissions: List[Permission]
	) -> List[Permission] | None:
		return await self.permission_usecase.find_permissions(permissions)

	def create_group(self, command: CreateGroupCommand) -> GroupPermission:
		return self.permission_usecase.create_group(command)

	@Transactional()
	async def append_permissions_to_group(
		self, permissions: List[Permission], id_group: int
	) -> GroupPermission:
		return await self.permission_usecase.append_permissions_to_group(permissions, id_group)

	#FIXME: Esto no deberia llamar a permission_repository
	async def get_all_groups(self) -> List[GroupPermission]:
		return await self.permission_usecase.permission_repository.get_all_groups()

	#FIXME: Esto no deberia llamar a permission_repository
	async def get_group_by_id(
		self, id_group: int, with_permissions: bool = False, with_roles: bool = False
	) -> GroupPermission:
		group = await self.permission_usecase.permission_repository.get_group_by_id(
			id_group, with_permissions, with_roles
		)
		if not group:
			raise GroupNotFoundException
		return group
	
	#FIXME: Esto no deberia llamar a permission_repository
	@Transactional()
	async def save_group(self, group: GroupPermission) -> GroupPermission:
		return await self.permission_usecase.permission_repository.save_group(group)

	#FIXME: Esto no deberia llamar a permission_repository
	@Transactional()
	async def delete_group(self, group: GroupPermission) -> None:
		group = await self.permission_usecase.permission_repository.get_group_by_id(group.id)
		if not group:
			raise GroupNotFoundException
		return await self.permission_usecase.permission_repository.delete_group(group)

	async def extract_token_from_permissions(self, permissions: List[Permission]) -> List[str]:
		return [permission.token for permission in permissions]