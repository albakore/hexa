from abc import ABC, abstractmethod
from typing import List
from app.rbac.domain.entity.role import Role


class RoleUseCase(ABC):
	
	@abstractmethod
	def get_all_roles(self) -> List[Role]:
		raise NotImplementedError
	
	@abstractmethod
	def get_role_by_id(self, id_role: int) -> Role | None:
		raise NotImplementedError
	
	@abstractmethod
	def modify_role(self, role: Role) -> Role | None:
		raise NotImplementedError
	
	@abstractmethod
	def link_group_to_role(self, id_role: int, id_group: int) -> Role | None:
		raise NotImplementedError
	
	@abstractmethod
	def unlink_group_from_role(self, id_role: int, id_group: int) -> Role | None:
		raise NotImplementedError
	
	@abstractmethod
	def link_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		raise NotImplementedError
	
	@abstractmethod
	def unlink_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		raise NotImplementedError
	
	@abstractmethod
	def delete(self, id_role: int) -> None:
		raise NotImplementedError
	
	@abstractmethod
	def save(self, role: Role) -> None:
		raise NotImplementedError
