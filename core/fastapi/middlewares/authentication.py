import jwt
from pydantic import BaseModel, Field
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
	AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from starlette.authentication import BaseUser, AuthCredentials
from core.config.settings import env


class CurrentUser(BaseUser):
	def __init__(
		self,
		user_id: int | None,
		username: str | None,
		email: str | None,
		role: str | None,
	):
		self.id = user_id
		self.username = username
		self.email = email
		self.role = role

	@property
	def is_authenticated(self) -> bool:
		return self.id is not None

	@property
	def display_name(self) -> str:
		return f"User {self.id}" if self.id else "Anon"


class AuthBackend(AuthenticationBackend):
	async def authenticate(
		self, conn: HTTPConnection
	) -> tuple[AuthCredentials, CurrentUser] | None:
		authorization: str | None = conn.headers.get("Authorization")
		if not authorization:
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
			user_id = payload.get("user_id")
		except jwt.exceptions.PyJWTError:
			print("Token inválido")
			return None

		return AuthCredentials(["authenticated"]), CurrentUser(user_id)


class AuthenticationMiddleware(BaseAuthenticationMiddleware): ...
