from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Sequence
from app.module.domain.entity.module import Module
from app.module.domain.repository.module import AppModuleRepository
from app.rbac.domain.command import CreateRoleCommand
from app.rbac.domain.entity import GroupPermission, Permission
from app.rbac.domain.entity.role import Role
from app.rbac.domain.exception import RoleNotFoundException
from app.rbac.domain.repository.permission import PermissionRepository
from app.rbac.domain.repository.role import RoleRepository
from core.db import Transactional


@dataclass
class GetAllRolesUseCase:
	role_repository: RoleRepository

	async def __call__(self) -> List[Role] | Sequence[Role]:
		return await self.role_repository.get_all_roles()


@dataclass
class GetRoleByIdUseCase:
	role_repository: RoleRepository

	async def __call__(
		self,
		id_role: int,
		with_permissions: bool = False,
		with_groups: bool = False,
		with_modules: bool = False,
	) -> Role | None:
		return await self.role_repository.get_role_by_id(
			id_role,
			with_permissions,
			with_groups,
			with_modules,
		)


@dataclass
class DeleteRoleUseCase:
	role_repository: RoleRepository

	@Transactional()
	async def __call__(self, id: int) -> None:
		role = await self.role_repository.get_role_by_id(id)
		if not role:
			raise RoleNotFoundException
		await self.role_repository.delete_role(role)


@dataclass
class SaveRoleUseCase:
	role_repository: RoleRepository

	@Transactional()
	async def __call__(self, role: Role) -> Role | None:
		return await self.role_repository.save_role(role)


@dataclass
class CreateRoleUseCase:
	def __call__(self, command: CreateRoleCommand) -> Role:
		role = Role.model_validate(command)
		return role


@dataclass
class AppendPermissionsUseCase:
	def __call__(self, role: Role, permissions: List[Permission]) -> None:
		for permission in permissions:
			role.permissions.append(permission)


@dataclass
class AppendPermissionsToRoleUseCase:
	role_repository: RoleRepository
	permission_repository: PermissionRepository

	@Transactional()
	async def __call__(self, permissions: List[Permission], id_role: int) -> Role:
		role = await self.role_repository.get_role_by_id(id_role, with_permissions=True)
		if not role:
			raise RoleNotFoundException

		permission_ids = [p.id for p in permissions]
		permissions_from_db = await self.permission_repository.get_permissions_by_ids(
			permission_ids  # type:ignore
		)

		for permission in permissions_from_db:
			if permission not in role.permissions:
				role.permissions.append(permission)

		return await self.role_repository.save_role(role)  # type: ignore


@dataclass
class AppendGroupsToRoleUseCase:
	role_repository: RoleRepository
	permission_repository: PermissionRepository

	@Transactional()
	async def __call__(self, groups: List[GroupPermission], id_role: int) -> Role:
		role = await self.role_repository.get_role_by_id(id_role, with_groups=True)
		if not role:
			raise RoleNotFoundException

		group_ids = [g.id for g in groups]
		groups_from_db = await self.permission_repository.get_groups_by_ids(
			group_ids  # type:ignore
		)

		for group in groups_from_db:
			if group not in role.groups:
				role.groups.append(group)

		return await self.role_repository.save_role(role)


@dataclass
class AppendModulesToRoleUseCase:
	role_repository: RoleRepository
	module_repository: AppModuleRepository

	@Transactional()
	async def __call__(self, modules: List[Module], id_role: int) -> Role:
		role = await self.role_repository.get_role_by_id(id_role, with_modules=True)
		if not role:
			raise RoleNotFoundException

		module_ids = [m.id for m in modules]
		modules_from_db = await self.module_repository.get_modules_by_ids(
			module_ids  # type:ignore
		)

		for module in modules_from_db:
			if module not in role.modules:
				role.modules.append(module)

		return await self.role_repository.save_role(role)


@dataclass
class GetModulesFromRoleUseCase:
	role_repository: RoleRepository

	async def __call__(self, role: Role) -> List[Module] | Sequence[Module]:
		return await self.role_repository.get_all_modules_from_role(role)


@dataclass
class GetAllRolesFromModulesUseCase:
	role_repository: RoleRepository

	async def __call__(self, modules_ids: List[int]) -> List[Role] | Sequence[Role]:
		return await self.role_repository.get_all_roles_from_modules(modules_ids)


@dataclass
class RemovePermissionsToRoleUseCase:
	role_repository: RoleRepository

	@Transactional()
	async def __call__(self, permissions: List[Permission], id_role: int) -> int:
		return await self.role_repository.remove_permissions_to_role(
			permissions, id_role
		)


@dataclass
class RemoveGroupPermissionsToRoleUseCase:
	role_repository: RoleRepository

	@Transactional()
	async def __call__(self, groups: List[GroupPermission], id_role: int) -> int:
		return await self.role_repository.remove_group_permissions_to_role(
			groups, id_role
		)


@dataclass
class RemoveModulesToRoleUseCase:
	role_repository: RoleRepository

	@Transactional()
	async def __call__(self, module_ids: List[int], id_role: int) -> int:
		return await self.role_repository.remove_modules_to_role(module_ids, id_role)


@dataclass
class RoleUseCaseFactory:
	role_repository: RoleRepository
	permission_repository: PermissionRepository
	module_repository: AppModuleRepository

	def __post_init__(self):
		self.get_all_roles = GetAllRolesUseCase(self.role_repository)
		self.get_role_by_id = GetRoleByIdUseCase(self.role_repository)
		self.delete_role = DeleteRoleUseCase(self.role_repository)
		self.save_role = SaveRoleUseCase(self.role_repository)
		self.create_role = CreateRoleUseCase()
		self.append_permissions = AppendPermissionsUseCase()
		self.append_permissions_to_role = AppendPermissionsToRoleUseCase(
			self.role_repository, self.permission_repository
		)
		self.append_groups_to_role = AppendGroupsToRoleUseCase(
			self.role_repository, self.permission_repository
		)
		self.append_modules_to_role = AppendModulesToRoleUseCase(
			self.role_repository, self.module_repository
		)
		self.get_modules_from_role = GetModulesFromRoleUseCase(self.role_repository)
		self.get_all_roles_from_modules = GetAllRolesFromModulesUseCase(
			self.role_repository
		)
		self.remove_permissions_to_role = RemovePermissionsToRoleUseCase(
			self.role_repository
		)
		self.remove_group_permissions_to_role = RemoveGroupPermissionsToRoleUseCase(
			self.role_repository
		)
		self.remove_modules_to_role = RemoveModulesToRoleUseCase(self.role_repository)
