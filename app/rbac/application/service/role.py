from typing import List
from app.rbac.domain.entity.role import Role
from app.rbac.domain.usecase.role import RoleUseCase


class RoleService(RoleUseCase):
	
	def get_all_roles(self) -> List[Role]:
		raise NotImplementedError

	def get_role_by_id(self, id_role: int) -> Role | None:
		raise NotImplementedError

	def modify_role(self, role: Role) -> Role | None:
		raise NotImplementedError

	def link_group_to_role(self, id_role: int, id_group: int) -> Role | None:
		raise NotImplementedError

	def unlink_group_from_role(self, id_role: int, id_group: int) -> Role | None:
		raise NotImplementedError

	def link_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		raise NotImplementedError

	def unlink_grouplist_to_role(
		self, id_role: int, list_id_group: List[int]
	) -> Role | None:
		raise NotImplementedError

	def delete(self, id_role: int) -> None:
		raise NotImplementedError

	def save(self, role: Role) -> None:
		raise NotImplementedError
