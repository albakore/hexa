from typing import List

from sqlmodel import select
from sqlalchemy.orm import selectinload
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
	):
		self.role_repository = role_repository
		self.permission_repository = permission_repository

	async def get_all_roles(self) -> list[Role]:
		return await self.role_repository.get_all_roles()

	async def get_role_by_id(self, id_role: int) -> Role | None:
		return await self.role_repository.get_role_by_id(id_role)

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

	@Transactional()
	async def delete(self, role: Role) -> None:
		return await self.role_repository.delete_role(role)

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
