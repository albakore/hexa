from sqlalchemy.orm import selectinload
from sqlmodel import or_, select, col
from typing import List, Sequence
from app.rbac.application.exception import RoleNotFoundException
from app.rbac.domain.entity.permission import Permission
from app.rbac.domain.entity import (
	GroupPermission,
	GroupPermissionLink,
	Role,
	RoleGroupPermissionLink,
)
from app.rbac.domain.repository import RoleRepository, PermissionRepository
from core.db import session_factory, session as global_session


class RBACSQLAlchemyRepository(RoleRepository, PermissionRepository):
	async def get_all_permissions(self) -> List[Permission] | Sequence[Permission]:
		stmt = select(Permission)
		async with session_factory() as session:
			result = await session.execute(stmt)
		return result.scalars().all()

	async def get_permission_by_id(self, id_permission: int) -> Permission | None:
		async with session_factory() as session:
			instance = await session.get(Permission, int(id_permission))
		return instance
	
	async def get_permissions_by_ids(self, ids: list[int]) -> List[Permission] | Sequence[Permission]:
		if not ids:
			return []
		stmt = select(Permission).where(col(Permission.id).in_(ids))
		async with session_factory() as session:
			result = await session.execute(stmt)
		return result.scalars().all()

	async def get_all_permissions_from_role(
		self, role: Role
	) -> List[Permission] | Sequence[Permission] | None:
		stmt = (
			select(RoleGroupPermissionLink)
			.join(
				GroupPermissionLink,
				GroupPermissionLink.fk_group == RoleGroupPermissionLink.fk_group,
			)
			.where(RoleGroupPermissionLink.fk_role == role.id)
			.distinct()
		)

	async def link_permission_to_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		raise NotImplementedError

	async def unlink_permission_from_group(
		self, id_permission: int, id_group: int
	) -> GroupPermission | None:
		raise NotImplementedError

	async def link_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		raise NotImplementedError

	async def unlink_list_permissions_to_group(
		self, id_group: int, list_id_permission: List[int]
	) -> GroupPermission | None:
		raise NotImplementedError

	async def delete_permission(self, permission: Permission) -> None:
		await global_session.delete(permission)
		await global_session.flush()

	async def save_permission(self, permission: Permission) -> Permission | None:
		global_session.add(permission)
		await global_session.flush()
		return permission

	async def get_all_roles(self) -> List[Role] | Sequence[Role] | None:
		stmt = select(Role)
		async with session_factory() as session:
			result = await session.execute(stmt)
		return result.scalars().all()

	async def get_role_by_id(
		self, id_role: int, with_permissions: bool = False, with_groups: bool = False
	) -> Role | None:
		stmt = select(Role).where(Role.id == int(id_role))

		if with_permissions:
			stmt = stmt.options(selectinload(Role.permissions))  # type: ignore

		if with_groups:
			stmt = stmt.options(selectinload(Role.groups))  # type: ignore

		async with session_factory() as session:
			role = await session.execute(stmt)

		return role.scalars().one_or_none()

	async def link_group_to_role(self, id_role: int, id_group: int) -> Role | None:
		raise NotImplementedError

	async def unlink_group_from_role(self, id_role: int, id_group: int) -> Role | None:
		raise NotImplementedError

	async def link_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		raise NotImplementedError

	async def unlink_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		raise NotImplementedError

	async def delete_role(self, role: Role) -> None:
		await global_session.delete(role)
		await global_session.flush()

	async def save_role(self, role: Role) -> Role | None:
		global_session.add(role)
		await global_session.flush()
		return role

	async def append_permissions_to_role(
		self, permissions: List[Permission], id_role: int
	) -> Role:
		role = await global_session.get(Role, int(id_role))
		if not role:
			raise RoleNotFoundException
		for permission in permissions:
			role.permissions.append(permission)
		return role

	async def find_permissions(
		self, permissions: List[Permission]
	) -> List[Permission] | Sequence[Permission] | None:
		stmt = select(Permission).where(
			col(Permission.id).in_([item.id for item in permissions])
		)
		async with session_factory() as session:
			result = await session.execute(stmt)
		return result.scalars().all()
