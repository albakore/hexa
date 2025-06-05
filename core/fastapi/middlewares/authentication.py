from typing import List
import jwt
from pydantic import BaseModel, Field
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
	AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from starlette.authentication import BaseUser, AuthCredentials
from core.config.settings import env


class CurrentUser(BaseModel):
	id: int
	username: str
	email: str
	role: str
	tipo_usuario: str
	permissions: List[str]


class User(BaseUser):
	def __init__(self, user_data: CurrentUser):
		self._user = user_data

	@property
	def is_authenticated(self):
		return True

	def __getattr__(self, item):
		return getattr(self._user, item)


class AuthBackend(AuthenticationBackend):
	async def authenticate(
		self, conn: HTTPConnection
	) -> tuple[AuthCredentials, User] | None:
		authorization: str | None = conn.headers.get("Authorization")
		if not authorization:
			print("❌ Sin Authorization")
			return None

		try:
			scheme, credentials = authorization.split(" ")
			if scheme.lower() != "bearer":
				return None
		except ValueError:
			return None

		try:
			payload = jwt.decode(
				credentials,
				env.JWT_SECRET_KEY,
				algorithms=[env.JWT_ALGORITHM],
			)
			user = CurrentUser(**payload)
			scopes = user.permissions

		except jwt.exceptions.PyJWTError:
			print("Token inválido")
			return None

		return AuthCredentials(scopes), User(user)


class AuthenticationMiddleware(BaseAuthenticationMiddleware): ...
