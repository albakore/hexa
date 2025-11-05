"""
Protocolo para servicios del módulo RBAC.

Permite type checking y autocompletado sin crear dependencias directas
entre otros módulos.
"""

from typing import Any, List, Optional, Protocol, Self


class RoleServiceProtocol(Protocol):
	"""
	API pública del módulo RBAC para gestión de roles.

	Expone operaciones para gestión de roles, permisos y módulos.
	"""

	def __call__(self) -> Self: ...

	async def get_all_roles(self) -> List[Any]:
		"""Obtiene todos los roles"""
		...

	async def get_role_by_id(
		self,
		id_role: int,
		with_permissions: bool = False,
		with_groups: bool = False,
		with_modules: bool = False,
	) -> Optional[Any]:
		"""
		Obtiene un rol por ID.

		Used by: auth (jwt refresh token)
		"""
		...

	async def get_permissions_from_role(self, role: Any) -> List[Any]:
		"""
		Obtiene todos los permisos de un rol.

		Used by: auth (login, jwt refresh)
		"""
		...

	async def get_modules_from_role_entity(self, role: Any) -> List[Any]:
		"""
		Obtiene todos los módulos de un rol.

		Used by: auth (login, jwt refresh)
		"""
		...

	async def get_modules_from_role(self, role: Any) -> List[Any]:
		"""Obtiene módulos de un rol"""
		...

	async def create_role(self, command: Any) -> Any:
		"""Crea un nuevo rol"""
		...

	async def save(self, role: Any) -> Optional[Any]:
		"""Guarda un rol"""
		...

	async def delete(self, id: int) -> None:
		"""Elimina un rol"""
		...

	async def edit_role(self, id_role: int, command: Any) -> Any:
		"""Edita un rol existente"""
		...

	async def append_permissions_to_role(
		self, permissions: List[Any], id_role: int
	) -> Any:
		"""Añade permisos a un rol"""
		...

	async def append_groups_to_role(self, groups: List[Any], id_role: int) -> Any:
		"""Añade grupos de permisos a un rol"""
		...

	async def append_modules_to_role(self, modules: List[Any], id_role: int) -> Any:
		"""Añade módulos a un rol"""
		...

	async def remove_permissions_to_role(
		self, permissions: List[Any], id_role: int
	) -> int:
		"""Remueve permisos de un rol"""
		...

	async def remove_group_permissions_to_role(
		self, groups: List[Any], id_role: int
	) -> int:
		"""Remueve grupos de permisos de un rol"""
		...

	async def remove_modules_to_role(self, modules: List[Any], id_role: int) -> Any:
		"""Remueve módulos de un rol"""
		...

	async def get_all_roles_from_modules(self, id_modules: List[int]) -> List[Any]:
		"""Obtiene roles asociados a módulos específicos"""
		...


class PermissionServiceProtocol(Protocol):
	"""API pública del módulo RBAC para gestión de permisos"""

	def __call__(self) -> Self: ...

	async def get_all_permissions(self) -> List[Any]:
		"""Obtiene todos los permisos"""
		...

	async def get_permission_by_id(self, id: int) -> Optional[Any]:
		"""Obtiene un permiso por ID"""
		...
