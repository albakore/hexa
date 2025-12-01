import uuid

from modules.auth.domain.repository.auth import AuthRepository
from modules.auth.domain.entity import RecoverPassword
from modules.user.application.dto import LoginResponseDTO


class AuthRepositoryAdapter(AuthRepository):
	def __init__(
		self, redis_repository: AuthRepository, sqlalchemy_repository: AuthRepository
	):
		self.redis_repository = redis_repository
		self.sqlalchemy_repository = sqlalchemy_repository

	async def create_user_session(self, login_response_dto: LoginResponseDTO):
		return await self.redis_repository.create_user_session(login_response_dto)

	async def get_user_session(self, user_uuid: str):
		return await self.redis_repository.get_user_session(user_uuid)

	async def revoque_user_session(self, login_response_dto: LoginResponseDTO):
		return await self.redis_repository.revoque_user_session(login_response_dto)

	async def get_user_permissions(self, user_uuid: str):
		raise NotImplementedError

	async def delete_user_session(self, user_uuid: str):
		return await self.redis_repository.delete_user_session(user_uuid)

	async def create_recovery_password_request(
		self, recovery_request: RecoverPassword
	) -> RecoverPassword:
		return await self.sqlalchemy_repository.create_recovery_password_request(
			recovery_request
		)

	async def get_active_recovery_request(
		self, user_uuid: uuid.UUID
	) -> RecoverPassword | None:
		return await self.sqlalchemy_repository.get_active_recovery_request(user_uuid)

	async def mark_recovery_as_completed(self, recovery_id: uuid.UUID) -> None:
		return await self.sqlalchemy_repository.mark_recovery_as_completed(recovery_id)
