"""
Protocolo para servicios del módulo User.

Permite type checking y autocompletado sin crear dependencias directas
entre otros módulos.
"""

from typing import Any, List, Optional, Protocol, Self, Sequence


class UserServiceProtocol(Protocol):
	"""
	API pública del módulo User.

	Expone operaciones para gestión de usuarios.
	"""

	def __call__(self) -> Self: ...

	async def get_user_list(self, limit: int | None = None, page: int = 0) -> List[Any]:
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

		Used by: auth (login, register)
		"""
		...

	async def save_user(self, user: Any) -> Any:
		"""
		Guarda un usuario.

		Used by: auth (register)
		"""
		...

	async def set_user_password(self, user: Any, hashed_password: str) -> Any:
		"""
		Establece la contraseña de un usuario.

		Used by: auth (password reset)
		"""
		...

	async def create_user(self, command: Any) -> Optional[Any]:
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
