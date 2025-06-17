from typing import List
from app.rbac.domain.command import CreatePermissionCommand
from app.rbac.domain.entity import Permission, Role
from app.rbac.domain.entity import GroupPermission
from app.rbac.domain.repository import PermissionRepository
from app.rbac.domain.usecase import PermissionUseCase
from core.db import Transactional


class PermissionService(PermissionUseCase):

	def __init__(self, permission_repository : PermissionRepository):
		self.permission_repository = permission_repository

	async def get_all_permissions(self) -> List[Permission]:
		return await self.permission_repository.get_all_permissions()

	async def get_permission_by_id(self, id_permission: int) -> Permission | None:
		return await self.permission_repository.get_permission_by_id(id_permission)

	async def link_permission_to_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		return await self.permission_repository.link_permission_to_group(id_permission,id_group)

	async def unlink_permission_from_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		return await self.permission_repository.unlink_permission_from_group(id_permission,id_group)

	async def link_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		return await self.permission_repository.link_list_permissions_to_group(id_group,list_id_permission)

	async def unlink_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		return await self.permission_repository.unlink_list_permissions_to_group(id_group,list_id_permission)

	@Transactional()
	async def delete(self, permission: Permission) -> None:
		return await self.permission_repository.delete_permission(permission)

	@Transactional()
	async def save(self, permission: Permission) -> None:
		return await self.permission_repository.save_permission(permission)

	async def get_all_permissions_from_role(self, role: Role) -> List[str] | None:
		permissions = await self.permission_repository.get_all_permissions_from_role(role)
		return permissions

	async def append_permission_to_role(self, permission: Permission, role: Role) -> Role | None:
		raise NotImplementedError

	async def modify_permission(self, permission: Permission) -> Permission | None:
		raise NotImplementedError

	def create_permission(self, command: CreatePermissionCommand) -> Permission:
		permission = Permission.model_validate(command)
		return permission

	async def find_permissions(self, permissions: List[Permission]) -> List[Permission] | None:
		return await self.permission_repository.find_permissions(permissions)



