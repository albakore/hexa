from dataclasses import dataclass

from fastapi.encoders import jsonable_encoder

from core.config.settings import env
from core.db.transactional import Transactional
from core.helpers.password import PasswordHelper
from core.helpers.token import TokenHelper
from modules.auth.application.dto import AuthPasswordResetResponseDTO
from modules.auth.application.exception import (
	AuthInitialPasswordResetError,
	AuthPasswordResetError,
	LoginUsernamePasswordException,
)
from modules.auth.application.usecase.auth import AuthUseCaseFactory
from modules.auth.domain.command import RegisterUserDTO
from modules.auth.domain.repository.auth import AuthRepository
from modules.module.application.dto import ModuleViewDTO
from modules.user.application.dto import LoginResponseDTO
from modules.user.application.dto.user import UserLoginResponseDTO
from modules.user.application.exception.user import (
	UserInactiveException,
	UserNotFoundException,
)

# Protocols compartidos desde shared/
from shared.interfaces.service_protocols import (
	EmailTemplateServiceProtocol,
	NotificationServiceProtocol,
	RoleServiceProtocol,
	UserServiceProtocol,
)


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
		self.usecase = AuthUseCaseFactory(self.user_service, self.auth_repository)

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

	@Transactional()
	async def recovery_password(self, email_or_nickname: str) -> bool:
		"""
		Crea una solicitud de recuperación de contraseña y envía un email al usuario
		con una contraseña temporal.

		Flujo:
		1. Genera una contraseña temporal
		2. La guarda hasheada en RecoverPassword
		3. Envía email con la contraseña temporal en texto plano
		4. Usuario debe llamar a complete_recovery_password con la temporal + nueva contraseña

		Args:
			email_or_nickname: Email o nickname del usuario que solicita la recuperación

		Returns:
			bool: True si se envió el email correctamente

		Raises:
			UserNotFoundException: Si el usuario no existe
		"""
		# Buscar el usuario por email o nickname
		user = await self.user_service.get_user_by_email_or_nickname(
			email=email_or_nickname, nickname=email_or_nickname
		)

		if not user:
			raise UserNotFoundException

		# Crear la solicitud de recuperación (guarda el registro en BD con contraseña hasheada)
		recovery_request = await self.usecase.create_recovery_password_request(
			user_uuid=user.id  # type: ignore
		)

		await self.notification_service.send_email_notification(
			{
				"template_name": "recover_password",
				"notification": {
					"to": [user.email],
					"subject": "Reset password",
				},
				"data_injection": {
					"name": user.name,
					"redirect_url": f"{env.FRONTEND_URL}?email={user.email}&temp={recovery_request.temporary_password_plain}",
				},
			}
		)
		return True

	@Transactional()
	async def complete_recovery_password(
		self, email_or_nickname: str, temporary_password: str, new_password: str
	) -> bool:
		"""
		Completa el proceso de recuperación de contraseña validando la contraseña
		temporal contra el registro de RecoverPassword.

		Args:
			email_or_nickname: Email o nickname del usuario
			temporary_password: Contraseña temporal recibida por email
			new_password: Nueva contraseña elegida por el usuario

		Returns:
			bool: True si se completó exitosamente

		Raises:
			UserNotFoundException: Si el usuario no existe
			ValueError: Si la contraseña temporal es inválida o expiró
		"""
		# Buscar el usuario
		user = await self.user_service.get_user_by_email_or_nickname(
			email=email_or_nickname, nickname=email_or_nickname
		)

		if not user:
			raise UserNotFoundException

		# Completar la recuperación usando el caso de uso
		await self.usecase.complete_recovery_password(
			user_uuid=user.id,  # type: ignore
			temporary_password=temporary_password,
			new_password=new_password,
		)

		return True

	### TODO ofrecer un servicio que sea get_user_session -> LoginResponseDTO | AuthPasswordResetResponseDTO

	async def get_user_session(self, user_uuid: str):
		session = await self.usecase.get_session_user(user_uuid)
		return session

	def _prepare_template(self, template: bytes, data: dict) -> str:
		template_decoded = template.decode()
		for key, value in data.items():
			template_decoded = template_decoded.replace(key, value)
		return template_decoded
