from sqlalchemy.orm import selectinload
from sqlmodel import or_, select, col
from typing import List, Sequence
from app.module.domain.entity.module import Module, ModuleRoleLink
from app.rbac.application.exception import RoleNotFoundException
from app.rbac.domain.entity.permission import Permission
from app.rbac.domain.entity import (
	GroupPermission,
	GroupPermissionLink,
	Role,
	RoleGroupPermissionLink,
)
from app.rbac.domain.entity.role import RolePermissionLink
from app.rbac.domain.repository import (
	RBACRepository,
	RoleRepository,
	PermissionRepository,
)
from core.db import session_factory, session as global_session


class RBACSQLAlchemyRepository(RBACRepository):
	async def get_all_permissions(self) -> List[Permission] | Sequence[Permission]:
		stmt = select(Permission)
		async with session_factory() as session:
			result = await session.execute(stmt)
		return result.scalars().all()

	async def get_permission_by_id(self, id_permission: int) -> Permission | None:
		async with session_factory() as session:
			instance = await session.get(Permission, int(id_permission))
		return instance

	async def get_permissions_by_ids(
		self, ids: list[int]
	) -> List[Permission] | Sequence[Permission]:
		if not ids:
			return []
		stmt = select(Permission).where(col(Permission.id).in_(ids))
		async with session_factory() as session:
			result = await session.execute(stmt)
		return result.scalars().all()

	async def get_all_permissions_from_role(
		self, role: Role
	) -> List[Permission] | Sequence[Permission] | None:
		if not role.id:
			return []

		subq1 = select(RolePermissionLink.fk_permission).where(
			RolePermissionLink.fk_role == role.id
		)
		group_ids_subq = select(RoleGroupPermissionLink.fk_group).where(
			RoleGroupPermissionLink.fk_role == role.id
		)
		subq2 = select(GroupPermissionLink.fk_permission).where(
			col(GroupPermissionLink.fk_group).in_(group_ids_subq)
		)

		query = select(Permission).where(
			or_(col(Permission.id).in_(subq1), col(Permission.id).in_(subq2))
		)
		async with session_factory() as session:
			result = await session.execute(query)
		return result.scalars().all()

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
		self,
		id_role: int,
		with_permissions: bool = False,
		with_groups: bool = False,
		with_modules: bool = False,
	) -> Role | None:
		stmt = select(Role).where(Role.id == int(id_role))

		if with_permissions:
			stmt = stmt.options(selectinload(Role.permissions))  # type: ignore

		if with_groups:
			stmt = stmt.options(selectinload(Role.groups))  # type: ignore

		if with_modules:
			stmt = stmt.options(selectinload(Role.modules))  # type: ignore

		async with session_factory() as session:
			role = await session.execute(stmt)

		return role.scalars().one_or_none()

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
	) -> List[Permission] | Sequence[Permission]:
		stmt = select(Permission).where(
			col(Permission.id).in_([item.id for item in permissions])
		)
		async with session_factory() as session:
			result = await session.execute(stmt)
		return result.scalars().all()

	async def get_group_by_id(
		self, id_group: int, with_permissions: bool = False, with_roles: bool = False
	) -> GroupPermission | None:
		stmt = select(GroupPermission).where(GroupPermission.id == int(id_group))

		if with_permissions:
			stmt = stmt.options(selectinload(GroupPermission.permissions))  # type: ignore

		if with_roles:
			stmt = stmt.options(selectinload(GroupPermission.roles))  # type: ignore

		async with session_factory() as session:
			group = await session.execute(stmt)

		return group.scalars().one_or_none()

	async def get_all_groups(self) -> List[GroupPermission] | Sequence[GroupPermission]:
		stmt = select(GroupPermission)
		async with session_factory() as session:
			result = await session.execute(stmt)
		return result.scalars().all()

	async def get_groups_by_ids(
		self, ids: List[int]
	) -> List[GroupPermission] | Sequence[GroupPermission]:
		if not ids:
			return []
		stmt = select(GroupPermission).where(col(GroupPermission.id).in_(ids))
		async with session_factory() as session:
			result = await session.execute(stmt)
		return result.scalars().all()

	async def save_group(self, group: GroupPermission) -> GroupPermission:
		global_session.add(group)
		await global_session.flush()
		return group

	async def delete_group(self, group: GroupPermission) -> None:
		await global_session.delete(group)
		await global_session.flush()

	async def append_modules_to_role(self, modules: List[Module], id_role: int) -> Role:
		role = await global_session.get(Role, int(id_role))
		if not role:
			raise RoleNotFoundException
		for module in modules:
			role.modules.append(module)
		return role

	async def get_all_modules_from_role(self, role: Role) -> List[Module] | Sequence[Module]:
		if not role.id:
			return []

		subq1 = select(ModuleRoleLink.fk_module).where(
			ModuleRoleLink.fk_role == role.id
		)
		subq2 = select(Module).where(
			col(Module.id).in_(subq1)
		)

		async with session_factory() as session:
			result = await session.execute(subq2)
		return result.scalars().all()