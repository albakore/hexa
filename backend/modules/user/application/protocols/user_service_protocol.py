"""
Protocol para UserService - Define la API pública del módulo User.

Este protocol es mantenido por el equipo del módulo User y representa
el contrato que otros módulos pueden usar para interactuar con User.
"""

from typing import Protocol, Optional, List, Sequence, Any


class UserServiceProtocol(Protocol):
	"""
	API pública del módulo User.

	Este protocol define todos los métodos que otros módulos pueden usar
	para interactuar con el servicio de usuarios sin crear dependencias directas.
	"""

	async def get_user_list(self, limit: int, page: int) -> List[Any]:
		"""Obtiene lista de usuarios paginada"""
		...

	async def get_user_by_id(self, user_id: int) -> Optional[Any]:
		"""Obtiene usuario por ID"""
		...

	async def get_user_by_uuid(self, user_uuid: str) -> Optional[Any]:
		"""Obtiene usuario por UUID"""
		...

	async def get_user_by_email_or_nickname(
		self, email: str, nickname: str, with_role: bool = False
	) -> Optional[Any]:
		"""
		Obtiene usuario por email o nickname.

		Args:
			email: Email del usuario
			nickname: Nickname del usuario
			with_role: Si debe incluir información del rol

		Returns:
			User si existe, None si no

		Used by: auth module (login, register)
		"""
		...

	async def save_user(self, user: Any) -> Any:
		"""
		Guarda un usuario.

		Used by: auth module (register)
		"""
		...

	async def set_user_password(self, user: Any, hashed_password: str) -> Any:
		"""
		Establece la contraseña de un usuario.

		Used by: auth module (password reset)
		"""
		...

	async def create_user(self, *, command: Any) -> Optional[Any]:
		"""Crea un nuevo usuario"""
		...

	async def asign_role_to_user(self, user_uuid: str, role_id: int) -> Any:
		"""Asigna un rol a un usuario"""
		...

	async def get_all_user_with_roles(
		self, role_id_list: List[int]
	) -> List[Any] | Sequence[Any]:
		"""Obtiene todos los usuarios con roles específicos"""
		...
