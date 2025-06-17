from abc import ABC, abstractmethod
from typing import List
from app.rbac.domain.command import CreateRoleCommand
from app.rbac.domain.entity.role import Role


class RoleUseCase(ABC):
	
	@abstractmethod
	async def get_all_roles(self) -> List[Role]:
		raise NotImplementedError
	
	@abstractmethod
	async def get_role_by_id(self, id_role: int) -> Role | None:
		raise NotImplementedError
	
	@abstractmethod
	async def link_group_to_role(self, id_role: int, id_group: int) -> Role | None:
		raise NotImplementedError
	
	@abstractmethod
	async def unlink_group_from_role(self, id_role: int, id_group: int) -> Role | None:
		raise NotImplementedError
	
	@abstractmethod
	async def link_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		raise NotImplementedError
	
	@abstractmethod
	async def unlink_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
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
