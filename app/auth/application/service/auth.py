from fastapi.encoders import jsonable_encoder
from app.auth.application.dto import (
	AuthPasswordResetResponseDTO,
	AuthRegisterRequestDTO,
)
from app.auth.application.exception import (
	AuthInitialPasswordResetError,
	AuthPasswordResetError,
	LoginRequiresPasswordResetException,
	LoginUsernamePasswordException,
)
from app.auth.domain.entity.auth import AuthRepository
from app.auth.domain.usecase.auth import AuthUseCase
from app.user.application.dto import LoginResponseDTO
from app.user.application.dto.user import UserLoginResponseDTO
from app.user.application.exception.user import (
	UserInactiveException,
	UserNotFoundException,
	UserRegisteredException,
)
from app.user.domain.repository.user import UserRepository
from app.user.domain.entity.user import User
from core.db.transactional import Transactional
from core.helpers.password import PasswordHelper
from core.helpers.token import TokenHelper


class AuthService(AuthUseCase):
	def __init__(self, db_repository: AuthRepository, user_repository: UserRepository):
		self.db_repository = db_repository
		self.user_repository = user_repository

	async def login(
		self, email_or_nickname: str, password: str
	) -> LoginResponseDTO | AuthPasswordResetResponseDTO:
		user = await self.user_repository.get_user_by_email_or_nickname(
			email=email_or_nickname,
			nickname=email_or_nickname,
		)
		if not user:
			raise LoginUsernamePasswordException

		if not user.requires_password_reset and password == user.initial_password:
			raise LoginUsernamePasswordException

		if user.requires_password_reset and password == user.initial_password:
			return AuthPasswordResetResponseDTO.model_validate(user.model_dump())

		is_password_valid = PasswordHelper.verify_password(password, user.password)

		if not is_password_valid:
			raise LoginUsernamePasswordException

		if not user.is_active:
			raise UserInactiveException

		user_response = UserLoginResponseDTO.model_validate(user.model_dump())
		user_dump = jsonable_encoder(user_response)
		response = LoginResponseDTO(
			user=user_response,
			token=TokenHelper.encode(
				payload=user_dump,
				expire_period=TokenHelper.get_expiration_minutes()
			),
			refresh_token=TokenHelper.encode(
				payload={**user_dump, "sub": "refresh"},
				expire_period=TokenHelper.get_expiration_days()
			),
		)
		await self.db_repository.create_user_session(response)
		return response

	@Transactional()
	async def register(self, registration_data: AuthRegisterRequestDTO):
		user = await self.user_repository.get_user_by_email_or_nickname(
			email=registration_data.email, nickname=registration_data.nickname or ""
		)

		if user:
			raise UserRegisteredException

		new_user = User.model_validate(registration_data)
		user_created = await self.user_repository.save(new_user)
		return user_created

	@Transactional()
	async def password_reset(
		self, user_uuid: str, initial_password: str, new_password: str
	) -> bool | Exception:
		user = await self.user_repository.get_user_by_uuid(user_uuid)

		if not user:
			raise UserNotFoundException

		if initial_password != user.initial_password:
			raise AuthInitialPasswordResetError

		if not user.requires_password_reset:
			raise LoginUsernamePasswordException

		if not new_password:
			raise AuthPasswordResetError

		hashed_password = PasswordHelper.get_password_hash(new_password)

		await self.user_repository.set_user_password(user, hashed_password)
		return True
