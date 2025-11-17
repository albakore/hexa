"""
Protocolo para servicios del módulo Auth.

Permite type checking y autocompletado sin crear dependencias directas
entre otros módulos.
"""

from typing import Any, Protocol, Self


class AuthServiceProtocol(Protocol):
	"""API pública del módulo Auth para autenticación"""

	def __call__(self) -> Self: ...
	async def login(self, email_or_nickname: str, password: str) -> Any:
		"""
		Realiza login de usuario.

		Returns:
			LoginResponseDTO o AuthPasswordResetResponseDTO
		"""
		...

	async def register(self, registration_data: Any) -> Any:
		"""Registra un nuevo usuario"""
		...

	async def password_reset(
		self, user_uuid: str, initial_password: str, new_password: str
	) -> bool:
		"""Resetea la contraseña de un usuario"""
		...

	async def get_user_session(self, user_uuid: str) -> Any:
		"""Trae la sesión de un usuario"""
		...


class JwtServiceProtocol(Protocol):
	"""API pública del módulo Auth para gestión de JWT tokens"""

	def __call__(self) -> Self: ...
	async def verify_token(self, token: str) -> dict:
		"""Verifica y decodifica un JWT token"""
		...

	async def create_refresh_token(self, refresh_token: str) -> Any:
		"""
		Crea nuevo access token desde refresh token.

		Returns:
			RefreshTokenResponseDTO
		"""
		...
