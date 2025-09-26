from typing import List
import uuid
from dependency_injector.wiring import inject
import jwt
from pydantic import BaseModel, Field
import rich
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
	AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from starlette.authentication import BaseUser, AuthCredentials
from core.config.settings import env
from shared.interfaces.service_locator import service_locator


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
	def __init__(self):
		self._auth_repository = None

	@property
	def auth_repository(self):
		if self._auth_repository is None:
			self._auth_repository = service_locator.get_service("auth_repository")
		return self._auth_repository

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
			print("Error: no tiene bearer")
			return None

		if not credentials:
			return None
		try:
			payload = jwt.decode(
				credentials,
				env.JWT_SECRET_KEY,
				algorithms=[env.JWT_ALGORITHM],
			)
			user_uuid = payload["id"]
			user = CurrentUser(**payload)

			# Intentar obtener sesión si el repositorio está disponible
			if self.auth_repository:
				try:
					session = await self.auth_repository.get_user_session(user_uuid)
					if session:
						user.permissions = session.permissions
				except Exception:
					pass  # Continuar sin permisos si falla

			scopes = user.permissions or []

		except jwt.exceptions.PyJWTError:
			print("❌ Token inválido")

			return None

		authenticated_user = User(user)
		return AuthCredentials(scopes), authenticated_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware): ...
