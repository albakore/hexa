
from abc import ABC, abstractmethod
from typing import List

from app.rbac.domain.entity import Permission, Role
from app.rbac.domain.entity import GroupPermission


class PermissionRepository(ABC):
	
	@abstractmethod
	def get_all_permissions(self) -> List[Permission]: ...

	@abstractmethod
	def get_permission_by_id(self, id_permission: int ) -> Permission | None: ...

	@abstractmethod
	def get_all_permissions_from_role(self,role : Role) -> List[Permission] | None: ...	

	@abstractmethod
	def modify_permission(self, permission: Permission) -> Permission | None: ...

	@abstractmethod
	def link_permission_to_group(self, id_permission: int, id_group: int) -> GroupPermission | None: ...

	@abstractmethod
	def unlink_permission_from_group(self, id_permission: int, id_group: int) -> GroupPermission | None: ...

	@abstractmethod
	def link_list_permissions_to_group(self, id_group:int, list_id_permission: List[int]) -> GroupPermission | None: ...
	
	@abstractmethod
	def unlink_list_permissions_to_group(self, id_group:int, list_id_permission: List[int]) -> GroupPermission | None: ...

	@abstractmethod
	def delete(self, id_permission: int) -> None: ...

	@abstractmethod
	def save(self, permission: Permission) -> None: ...