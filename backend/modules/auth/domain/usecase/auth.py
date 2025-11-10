from dataclasses import dataclass

from modules.auth.domain.command import RegisterUserDTO
from modules.auth.domain.exception import RegisteredUserException
from modules.auth.domain.repository.auth import AuthRepository
from shared.interfaces.service_protocols import UserServiceProtocol

class UseCase: ...

@dataclass
class RegisterUser(UseCase):
	user_service : UserServiceProtocol

	async def __call__(self, registration_data: RegisterUserDTO):

		user = await self.user_service.get_user_by_email_or_nickname(
			email=registration_data.email, nickname=registration_data.nickname or ""
		)
		if user:
			raise RegisteredUserException
		user_created = await self.user_service.create_user(registration_data)
		return user_created

@dataclass
class GetSessionUser(UseCase):
	auth_repository : AuthRepository

	async def __call__(self, user_uuid: str):

		session = await self.auth_repository.get_user_session(user_uuid)
		return session

@dataclass
class AuthUseCaseFactory:
	user_service : UserServiceProtocol
	auth_repository : AuthRepository

	def __post_init__(self):
		self.register_user = RegisterUser(self.user_service)
		self.get_session_user = GetSessionUser(self.auth_repository)
