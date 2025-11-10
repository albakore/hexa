import uuid
from typing import List

import jwt
from pydantic import BaseModel
from starlette.authentication import AuthCredentials, AuthenticationBackend, BaseUser
from starlette.middleware.authentication import (
	AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from core.config.settings import env
from core.exceptions.authentication import (
	AuthDecodeTokenException,
	AuthExpiredTokenException,
	InvalidAuthorizationFormatException,
	InvalidSignatureException,
)
from shared.interfaces.service_protocols.auth import AuthServiceProtocol


class CurrentUser(BaseModel):
	id: uuid.UUID
	nickname: str
	email: str
	role: str | None = None
	permissions: List[str] | None = None


class User(BaseUser):
	def __init__(self, user_data: CurrentUser):
		self._user = user_data

	@property
	def is_authenticated(self):
		return True

	def __getattr__(self, item):
		return getattr(self._user, item)


class AuthBackend(AuthenticationBackend):
	def __init__(self, user_service: AuthServiceProtocol):
		self.user_service = user_service()
		self.last_exception: Exception | None = None

	async def authenticate(
		self, conn: HTTPConnection
	) -> tuple[AuthCredentials, User] | None:
		# Limpiar excepción anterior
		self.last_exception = None
		authorization: str | None = conn.headers.get("Authorization")

		if not authorization:
			print("❌ Sin Authorization")
			return None

		# Validar formato del header Authorization
		try:
			scheme, credentials = authorization.split(" ")
			if scheme.lower() != "bearer":
				print("❌ Esquema de autorización inválido")
				self.last_exception = InvalidAuthorizationFormatException()
				return None
		except ValueError:
			print("❌ Formato de Authorization inválido")
			self.last_exception = InvalidAuthorizationFormatException()
			return None

		if not credentials:
			print("❌ Token vacío")
			self.last_exception = InvalidAuthorizationFormatException()
			return None

		# Decodificar y validar token JWT
		try:
			payload = jwt.decode(
				credentials,
				env.JWT_SECRET_KEY,
				algorithms=[env.JWT_ALGORITHM],
			)
			user_uuid = payload["id"]
			session = await self.user_service.get_user_session(user_uuid)
			user = CurrentUser(**payload)
			if session:
				user.permissions = session.permissions
			scopes = user.permissions

		except jwt.ExpiredSignatureError:
			print("❌ Token expirado")
			self.last_exception = AuthExpiredTokenException()
			return None

		except jwt.InvalidSignatureError:
			print("❌ Firma del token inválida")
			self.last_exception = InvalidSignatureException()
			return None

		except jwt.DecodeError:
			print("❌ Token malformado")
			self.last_exception = AuthDecodeTokenException()
			return None

		except jwt.InvalidTokenError:
			print("❌ Token inválido")
			self.last_exception = AuthDecodeTokenException()
			return None

		except Exception as e:
			print(f"❌ Error inesperado al validar token: {e}")
			self.last_exception = AuthDecodeTokenException()
			return None

		authenticated_user = User(user)
		return AuthCredentials(scopes), authenticated_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
	"""
	Middleware de autenticación personalizado que maneja excepciones específicas.

	Extiende el comportamiento del AuthenticationMiddleware de Starlette para
	propagar las excepciones específicas guardadas en el AuthBackend.
	"""

	async def __call__(self, scope, receive, send):
		"""
		Intercepta la llamada para capturar excepciones del backend.
		"""
		# Llamar al middleware padre
		await super().__call__(scope, receive, send)
