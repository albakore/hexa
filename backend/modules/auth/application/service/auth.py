from dataclasses import dataclass
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
from modules.auth.domain.command import RegisterUserDTO
from modules.auth.domain.repository.auth import AuthRepository
from modules.auth.domain.usecase.auth import AuthUseCaseFactory
from modules.module.application.dto import ModuleViewDTO
from modules.user.application.dto import LoginResponseDTO
from modules.user.application.dto.user import UserLoginResponseDTO
from modules.user.application.exception.user import (
	UserInactiveException,
	UserNotFoundException,
	UserRegisteredException,
)
from modules.user.domain.entity.user import User
from core.db.transactional import Transactional
from core.helpers.password import PasswordHelper
from core.helpers.token import TokenHelper

# Protocols compartidos desde shared/
from shared.interfaces.service_protocols import EmailTemplateServiceProtocol, NotificationCommandType, NotificationServiceProtocol, UserServiceProtocol, RoleServiceProtocol

@dataclass
class AuthService:
	auth_repository: AuthRepository
	user_service: UserServiceProtocol
	role_service: RoleServiceProtocol
	email_template_service: EmailTemplateServiceProtocol
	notification_service: NotificationServiceProtocol

	def __post_init__(self):
		self.user_service = self.user_service()
		self.role_service = self.role_service()
		self.email_template_service = self.email_template_service()
		self.notification_service = self.notification_service()
		self.usecase = AuthUseCaseFactory(
			self.user_service
		)

	async def login(
		self, email_or_nickname: str, password: str
	) -> LoginResponseDTO | AuthPasswordResetResponseDTO:
		user = await self.user_service.get_user_by_email_or_nickname(
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
			permissions = await self.role_service.get_permissions_from_role(user.role)
			modules = await self.role_service.get_modules_from_role_entity(user.role)

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

	async def register(self, registration_data: RegisterUserDTO):
		new_user = await self.usecase.register_user(registration_data)
		template = await self.email_template_service.get_email_template_by_name("email_registration")
		
		if not new_user:
			raise UserNotFoundException
		template_decoded = self._prepare_template(
			template,{
			"#PROVIDER_NAME#":  new_user.nickname or new_user.name,
			"#NAME#":  new_user.name,
			"#USERNAME#":  new_user.nickname or new_user.email,
			"#PASSWORD#":  new_user.initial_password,
		})
		data : NotificationCommandType ={
			"sender": "email",
			"notification": {
				"to":[new_user.email],
				"body":template_decoded,
				"subject":"User Registration"
			}
		}
		await self.notification_service.send_notification(data)
		return new_user

	@Transactional()
	async def password_reset(
		self, user_uuid: str, initial_password: str, new_password: str
	) -> bool | Exception:
		user = await self.user_service.get_user_by_uuid(user_uuid)

		if not user:
			raise UserNotFoundException

		if initial_password != user.initial_password:
			raise AuthInitialPasswordResetError

		if not user.requires_password_reset:
			raise LoginUsernamePasswordException

		if not new_password:
			raise AuthPasswordResetError

		hashed_password = PasswordHelper.get_password_hash(new_password)

		await self.user_service.set_user_password(user, hashed_password)
		return True
	
	#TODO agregar un recovery_password que notifique al usuario los pasos a seguir para reestablecerla
	#template email_recoverypassword

	def _prepare_template(self, template: bytes, data: dict) -> str:
		template_decoded = template.decode()
		for key, value in data.items():
			template_decoded = template_decoded.replace(key,value)
		return template_decoded
	