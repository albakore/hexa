from fastapi.encoders import jsonable_encoder
from modules.auth.application.dto import (
	AuthPasswordResetResponseDTO,
	AuthRegisterRequestDTO,
)
from modules.auth.application.exception import (
	AuthInitialPasswordResetError,
	AuthPasswordResetError,
	LoginRequiresPasswordResetException,
	LoginUsernamePasswordException,
)
from modules.auth.domain.repository.auth import AuthRepository
from modules.auth.domain.usecase.auth import AuthUseCase
from modules.module.application.dto import ModuleViewDTO
from modules.rbac.container import RoleService
from modules.rbac.domain.repository import (
	PermissionRepository,
	RBACRepository,
	RoleRepository,
)
from modules.user.application.dto import LoginResponseDTO
from modules.user.application.dto.user import UserLoginResponseDTO
from modules.user.application.exception.user import (
	UserInactiveException,
	UserNotFoundException,
	UserRegisteredException,
)
from modules.user.domain.repository.user import UserRepository
from modules.user.domain.entity.user import User
from core.db.transactional import Transactional
from core.helpers.password import PasswordHelper
from core.helpers.token import TokenHelper


class AuthService(AuthUseCase):
	def __init__(
		self,
		auth_repository: AuthRepository,
		user_repository: UserRepository,
		rbac_repository: RBACRepository,
	):
		self.auth_repository = auth_repository
		self.user_repository = user_repository
		self.rbac_repository = rbac_repository

	async def login(
		self, email_or_nickname: str, password: str
	) -> LoginResponseDTO | AuthPasswordResetResponseDTO:
		user = await self.user_repository.get_user_by_email_or_nickname(
			email=email_or_nickname, nickname=email_or_nickname, with_role=True
		)
		if not user:
			raise LoginUsernamePasswordException

		if not user.requires_password_reset and password == user.initial_password:
			raise LoginUsernamePasswordException

		if user.requires_password_reset and password == user.initial_password:
			return AuthPasswordResetResponseDTO.model_validate(user.model_dump())

		is_password_valid = PasswordHelper.verify_password(
			password, user.password or None
		)  # type: ignore

		if not is_password_valid:
			raise LoginUsernamePasswordException

		if not user.is_active:
			raise UserInactiveException

		user_response = UserLoginResponseDTO.model_validate(user.model_dump())
		user_dump = jsonable_encoder(user_response)
		permissions = []
		modules = []
		if user.role:
			permissions = await self.rbac_repository.get_all_permissions_from_role(
				user.role
			)
			modules = await self.rbac_repository.get_all_modules_from_role(user.role)

		response = LoginResponseDTO(
			user=user_response,
			permissions=[permission.token for permission in permissions],
			modules=[
				ModuleViewDTO.model_validate(module.model_dump()) for module in modules
			],
			token=TokenHelper.encode(
				payload=user_dump, expire_period=TokenHelper.get_expiration_minutes()
			),
			refresh_token=TokenHelper.encode(
				payload={**user_dump, "sub": "refresh"},
				expire_period=TokenHelper.get_expiration_days(),
			),
		)
		await self.auth_repository.create_user_session(response)
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
