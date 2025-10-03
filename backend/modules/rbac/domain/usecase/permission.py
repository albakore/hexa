from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from modules.rbac.application.service.role import PermissionRepository
from modules.rbac.domain.command import CreateGroupCommand, CreatePermissionCommand
from modules.rbac.domain.entity import Permission, Role
from modules.rbac.domain.entity import GroupPermission
from modules.rbac.domain.exception import GroupNotFoundException
from core.db import Transactional


@dataclass
class GetAllPermissionsUseCase:
	permission_repository: PermissionRepository

	async def __call__(self) -> List[Permission]:
		return await self.permission_repository.get_all_permissions()


@dataclass
class GetPermissionByIdUseCase:
	permission_repository: PermissionRepository

	async def __call__(self, id_permission: int) -> Permission | None:
		return await self.permission_repository.get_permission_by_id(id_permission)


@dataclass
class DeletePermissionUseCase:
	permission_repository: PermissionRepository

	@Transactional()
	async def __call__(self, permission: Permission) -> None:
		return await self.permission_repository.delete_permission(permission)


@dataclass
class SavePermissionUseCase:
	permission_repository: PermissionRepository

	@Transactional()
	async def __call__(self, permission: Permission) -> None:
		return await self.permission_repository.save_permission(permission)


@dataclass
class GetAllPermissionsFromRoleUseCase:
	permission_repository: PermissionRepository

	async def __call__(self, role: Role) -> List[str]:
		permissions = await self.permission_repository.get_all_permissions_from_role(role)
		return [permission.token for permission in permissions]


@dataclass
class ModifyPermissionUseCase:
	async def __call__(self, permission: Permission) -> Permission | None:
		raise NotImplementedError


@dataclass
class CreatePermissionUseCase:
	def __call__(self, command: CreatePermissionCommand) -> Permission:
		permission = Permission.model_validate(command)
		return permission


@dataclass
class FindPermissionsUseCase:
	permission_repository: PermissionRepository

	async def __call__(self, permissions: List[Permission]) -> List[Permission] | None:
		return await self.permission_repository.find_permissions(permissions)


@dataclass
class CreateGroupUseCase:
	def __call__(self, command: CreateGroupCommand) -> GroupPermission:
		group = GroupPermission.model_validate(command)
		return group


@dataclass
class AppendPermissionsToGroupUseCase:
	permission_repository: PermissionRepository

	@Transactional()
	async def __call__(self, permissions: List[Permission], id_group: int) -> GroupPermission:
		group = await self.permission_repository.get_group_by_id(id_group, with_permissions=True)
		if not group:
			raise GroupNotFoundException

		permission_ids = [p.id for p in permissions]
		permissions_from_db = await self.permission_repository.get_permissions_by_ids(permission_ids)

		for permission in permissions_from_db:
			if permission not in group.permissions:
				group.permissions.append(permission)
		return await self.permission_repository.save_group(group)


@dataclass
class PermissionUseCaseFactory:
	permission_repository: PermissionRepository

	def __post_init__(self):
		self.get_all_permissions = GetAllPermissionsUseCase(self.permission_repository)
		self.get_permission_by_id = GetPermissionByIdUseCase(self.permission_repository)
		self.delete_permission = DeletePermissionUseCase(self.permission_repository)
		self.save_permission = SavePermissionUseCase(self.permission_repository)
		self.get_all_permissions_from_role = GetAllPermissionsFromRoleUseCase(self.permission_repository)
		self.modify_permission = ModifyPermissionUseCase()
		self.create_permission = CreatePermissionUseCase()
		self.find_permissions = FindPermissionsUseCase(self.permission_repository)
		self.create_group = CreateGroupUseCase()
		self.append_permissions_to_group = AppendPermissionsToGroupUseCase(self.permission_repository)