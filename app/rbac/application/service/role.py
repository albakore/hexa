from typing import List

from sqlmodel import select
from sqlalchemy.orm import selectinload
from app.module.domain.entity.module import Module
from app.module.domain.repository.module import AppModuleRepository
from app.rbac.application.exception import RoleNotFoundException
from app.rbac.domain.command import CreateRoleCommand
from app.rbac.domain.entity import Permission
from app.rbac.domain.entity import GroupPermission, Role
from app.rbac.domain.repository import PermissionRepository, RoleRepository
from app.rbac.domain.usecase import PermissionUseCase
from app.rbac.domain.usecase import RoleUseCase
from core.db import Transactional, session_factory


class RoleService(RoleUseCase):
	def __init__(
		self,
		role_repository: RoleRepository,
		permission_repository: PermissionRepository,
		module_repository: AppModuleRepository,
	):
		self.role_repository = role_repository
		self.permission_repository = permission_repository
		self.module_repository = module_repository

	async def get_all_roles(self) -> list[Role]:
		return await self.role_repository.get_all_roles()

	async def get_role_by_id(
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


	@Transactional()
	async def delete(self, id: int) -> None:
		role = await self.role_repository.get_role_by_id(id)
		if not role:
			raise RoleNotFoundException
		await self.role_repository.delete_role(role)

	@Transactional()
	async def save(self, role: Role) -> Role | None:
		return await self.role_repository.save_role(role)

	async def create_role(self, command: CreateRoleCommand) -> Role:
		role = Role.model_validate(command)
		return role

	def append_permissions(self, role: Role, permissions: List[Permission]) -> None:
		for permission in permissions:
			role.permissions.append(permission)

	@Transactional()
	async def append_permissions_to_role(
		self, permissions: List[Permission], id_role: int
	) -> Role:
		role = await self.role_repository.get_role_by_id(id_role, with_permissions=True)
		if not role:
			raise RoleNotFoundException

		permission_ids = [p.id for p in permissions]

		permissions_from_db = await self.permission_repository.get_permissions_by_ids(
			permission_ids #type:ignore
		)

		for permission in permissions_from_db:
			if permission not in role.permissions:
				role.permissions.append(permission)

		return await self.role_repository.save_role(role)  # type: ignore

	@Transactional()
	async def append_groups_to_role(
		self, groups: List[GroupPermission], id_role: int
	) -> Role:
		role = await self.role_repository.get_role_by_id(id_role, with_groups=True)
		if not role:
			raise RoleNotFoundException

		group_ids = [g.id for g in groups]

		groups_from_db = await self.permission_repository.get_groups_by_ids(
			group_ids #type:ignore
		)

		for group in groups_from_db:
			if group not in role.groups:
				role.groups.append(group)

		return await self.role_repository.save_role(role)

	@Transactional()
	async def append_modules_to_role(self, modules: List[Module], id_role: int) -> Role:
		role = await self.role_repository.get_role_by_id(id_role, with_modules=True)
		if not role:
			raise RoleNotFoundException

		module_ids = [m.id for m in modules]

		modules_from_db = await self.module_repository.get_modules_by_ids(
			module_ids #type:ignore
		)

		for module in modules_from_db:
			if module not in role.modules:
				role.modules.append(module)

		return await self.role_repository.save_role(role)

	async def get_modules_from_role(self, role: Role) -> List[Module]:
		return await self.role_repository.get_all_modules_from_role(role)
