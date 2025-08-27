from dataclasses import dataclass
from typing import List

from app.module.domain.entity.module import Module
from app.module.domain.repository.module import AppModuleRepository
from app.rbac.application.exception import RoleNotFoundException
from app.rbac.domain.command import CreateRoleCommand, UpdateRoleCommand
from app.rbac.domain.entity import Permission
from app.rbac.domain.entity import GroupPermission, Role
from app.rbac.domain.repository import RoleRepository
from app.rbac.domain.repository.permission import PermissionRepository
from app.rbac.domain.usecase.role import RoleUseCaseFactory


@dataclass
class RoleService:
	role_repository: RoleRepository
	permission_repository: PermissionRepository
	module_repository: AppModuleRepository

	def __post_init__(self):
		self.role_usecase = RoleUseCaseFactory(
			self.role_repository, 
			self.permission_repository, 
			self.module_repository
		)

	async def get_all_roles(self) -> list[Role]:
		return await self.role_usecase.get_all_roles()

	async def get_role_by_id(
		self,
		id_role: int,
		with_permissions: bool = False,
		with_groups: bool = False,
		with_modules: bool = False,
	) -> Role | None:
		return await self.role_usecase.get_role_by_id(
			id_role,
			with_permissions,
			with_groups,
			with_modules,
		)

	async def delete(self, id: int) -> None:
		try:
			await self.role_usecase.delete_role(id)
		except RoleNotFoundException:
			raise

	async def edit_role(self,id_role: int, command: UpdateRoleCommand) -> Role:
		role = await self.role_usecase.get_role_by_id(id_role)
		if not role:
			raise RoleNotFoundException
		role.sqlmodel_update(command)
		return await self.role_usecase.save_role(role)

	async def save(self, role: Role) -> Role | None:
		return await self.role_usecase.save_role(role)

	async def create_role(self, command: CreateRoleCommand) -> Role:
		return self.role_usecase.create_role(command)

	def append_permissions(self, role: Role, permissions: List[Permission]) -> None:
		self.role_usecase.append_permissions(role, permissions)

	async def append_permissions_to_role(
		self, permissions: List[Permission], id_role: int
	) -> Role:
		return await self.role_usecase.append_permissions_to_role(permissions, id_role)

	async def append_groups_to_role(
		self, groups: List[GroupPermission], id_role: int
	) -> Role:
		return await self.role_usecase.append_groups_to_role(groups, id_role)

	async def append_modules_to_role(self, modules: List[Module], id_role: int) -> Role:
		return await self.role_usecase.append_modules_to_role(modules, id_role)

	async def get_modules_from_role(self, role: Role) -> List[Module]:
		return await self.role_usecase.get_modules_from_role(role)
	
	async def remove_permissions_to_role(self, permissions: List[Permission], id_role: int) -> int:
		return await self.role_usecase.remove_permissions_to_role(permissions,id_role)

	async def remove_group_permissions_to_role(self, groups: List[GroupPermission], id_role: int) -> int:
		return await self.role_usecase.remove_group_permissions_to_role(groups,id_role)

	async def remove_modules_to_role(self, modules: List[Module], id_role: int) -> Role:
		return await self.role_usecase.remove_modules_to_role(modules, id_role)

