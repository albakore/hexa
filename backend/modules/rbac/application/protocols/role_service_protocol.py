"""
Protocol para RoleService - Define la API pública del módulo RBAC.

Este protocol es mantenido por el equipo del módulo RBAC y representa
el contrato que otros módulos pueden usar para interactuar con RBAC.
"""

from typing import Protocol, Optional, List, Any


class RoleServiceProtocol(Protocol):
	"""
	API pública del módulo RBAC para gestión de roles.

	Este protocol define todos los métodos que otros módulos pueden usar
	para interactuar con roles y permisos sin crear dependencias directas.
	"""

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

		Args:
			id_role: ID del rol
			with_permissions: Incluir permisos
			with_groups: Incluir grupos de permisos
			with_modules: Incluir módulos asociados

		Returns:
			Role si existe, None si no

		Used by: auth module (jwt refresh token)
		"""
		...

	async def get_permissions_from_role(self, role: Any) -> List[Any]:
		"""
		Obtiene todos los permisos de un rol.

		Used by: auth module (login, jwt refresh)
		"""
		...

	async def get_modules_from_role_entity(self, role: Any) -> List[Any]:
		"""
		Obtiene todos los módulos de un rol.

		Used by: auth module (login, jwt refresh)
		"""
		...

	async def get_modules_from_role(self, role: Any) -> List[Any]:
		"""Obtiene módulos de un rol (alias)"""
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
