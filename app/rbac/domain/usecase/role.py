from abc import ABC, abstractmethod
from typing import List
from app.module.domain.entity.module import Module
from app.rbac.domain.command import CreateRoleCommand
from app.rbac.domain.entity import GroupPermission, Permission
from app.rbac.domain.entity.role import Role


class RoleUseCase(ABC):
	
	@abstractmethod
	async def get_all_roles(self) -> List[Role]:
		raise NotImplementedError

	@abstractmethod
	async def get_role_by_id(
		self,
		id_role: int,
		with_permissions: bool = False,
		with_groups: bool = False,
		with_modules: bool = False,
	) -> Role | None:
		raise NotImplementedError

	@abstractmethod
	async def delete(self, id_role: int) -> None:
		raise NotImplementedError

	@abstractmethod
	async def save(self, role: Role) -> Role | None:
		raise NotImplementedError

	@abstractmethod
	async def create_role(self, command: CreateRoleCommand) -> Role:
		raise NotImplementedError


	@abstractmethod
	def append_permissions(self,role: Role, permissions: List[Permission]) -> Role:
		raise NotImplementedError


	@abstractmethod
	async def append_permissions_to_role(
		self, permissions: List[Permission], id_role: int
	) -> Role:
		raise NotImplementedError

	@abstractmethod
	async def append_groups_to_role(
		self, groups: List[GroupPermission], id_role: int
	) -> Role:
		raise NotImplementedError

	@abstractmethod
	async def append_modules_to_role(
		self, modules: List[Module], id_role: int
	) -> Role:
		raise NotImplementedError