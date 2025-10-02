from app.auth.domain.repository.auth import AuthRepository
from modules.user.application.dto import LoginResponseDTO


class AuthRepositoryAdapter(AuthRepository):
	def __init__(self, repository: AuthRepository):
		self.repository = repository

	async def create_user_session(self, login_response_dto: LoginResponseDTO):
		return await self.repository.create_user_session(login_response_dto)

	async def get_user_session(self, user_uuid: str):
		return await self.repository.get_user_session(user_uuid)

	async def revoque_user_session(self, login_response_dto: LoginResponseDTO):
		return await self.repository.revoque_user_session(login_response_dto)

	async def get_user_permissions(self, user_uuid: str):
		raise NotImplementedError

	async def delete_user_session(self, user_uuid: str):
		return await self.repository.delete_user_session(user_uuid)
