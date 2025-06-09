

from app.auth.application.dto import AuthRegisterRequestDTO
from app.auth.application.exception import LoginUsernamePasswordException
from app.auth.domain.usecase.auth import AuthUseCase
from app.user.application.dto import LoginResponseDTO
from app.user.application.exception.user import UserNotFoundException
from app.user.domain.repository.user import UserRepository
from core.helpers.password import PasswordHelper
from core.helpers.token import TokenHelper


class AuthService(AuthUseCase):

	def __init__(self, user_repository : UserRepository):
		self.user_repository = user_repository

	async def login(self, *, email_or_nickname: str, password: str) -> LoginResponseDTO:
		user = await self.user_repository.get_user_by_email_or_nickname(
			email=email_or_nickname,
			nickname=email_or_nickname,
		)
		if not user:
			raise UserNotFoundException
		
		is_password_valid = PasswordHelper.verify_password(
			password,
			user.password or '*'
		)

		if not is_password_valid:
			raise LoginUsernamePasswordException


		response = LoginResponseDTO(
			token=TokenHelper.encode(payload={"user_id": user.id}),
			refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
		)
		return response
	
	async def register(self, registration_data : AuthRegisterRequestDTO):
		...
