from datetime import datetime, timedelta
import json

from fastapi.encoders import jsonable_encoder
from lzl.api.aioreq import delete
from redis.asyncio import Redis
import rich
from modules.auth.domain.repository.auth import AuthRepository
from modules.user.application.dto import LoginResponseDTO


class RedisAuthRepository(AuthRepository):
	session_prefix = "session"
	permission_prefix = "permission"
	days_of_expiration = 7

	def __init__(self, session_repository: Redis, permission_repository: Redis):
		self.session_repository = session_repository
		self.permission_repository = permission_repository

	async def create_user_session(self, login_response_dto: LoginResponseDTO):
		expiration_time = datetime.now() + timedelta(days=self.days_of_expiration)
		ttl_seconds = int((expiration_time - datetime.now()).total_seconds())

		status = await self.session_repository.set(
			f"{self.session_prefix}:{login_response_dto.user.id}",  # type: ignore
			login_response_dto.model_dump_json(),
			ex=ttl_seconds,
		)
		print(f" ++ [{status}] Session created for: {login_response_dto.user.id}")

	async def get_user_session(self, user_uuid: str):
		session = await self.session_repository.get(
			f"{self.session_prefix}:{user_uuid}"
		)
		if isinstance(session, str):
			session = LoginResponseDTO.model_validate_json(jsonable_encoder(session))
			return session
		return None

	async def revoque_user_session(self, login_response_dto: LoginResponseDTO):
		status = await self.session_repository.set(
			f"{self.session_prefix}:{login_response_dto.user.id}",  # type: ignore
			login_response_dto.model_dump_json(),
			keepttl=True,
		)
		print(f" ~~ [{status}] Session revoqued for: {login_response_dto.user.id}")

	async def get_user_permissions(self, user_uuid: str):
		raise NotImplementedError

	async def delete_user_session(self, user_uuid: str):
		status = await self.session_repository.delete(
			f"{self.session_prefix}:{user_uuid}"
		)
		print(f" -- [{status}] Session deleted for: {user_uuid}")
