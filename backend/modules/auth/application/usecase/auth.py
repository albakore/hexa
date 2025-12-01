import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

from core.helpers.password import PasswordHelper
from modules.auth.domain.command import RegisterUserDTO
from modules.auth.domain.entity import RecoverPassword
from modules.auth.domain.exception import RegisteredUserException
from modules.auth.domain.repository.auth import AuthRepository
from shared.interfaces.service_protocols import UserServiceProtocol


class UseCase: ...


@dataclass
class RegisterUser(UseCase):
	user_service: UserServiceProtocol

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
	auth_repository: AuthRepository

	async def __call__(self, user_uuid: str):
		session = await self.auth_repository.get_user_session(user_uuid)
		return session


@dataclass
class CreateRecoveryPasswordRequest(UseCase):
	auth_repository: AuthRepository
	user_service: UserServiceProtocol

	async def __call__(
		self, user_uuid: uuid.UUID, expiration_hours: int = 24
	) -> RecoverPassword:
		"""
		Crea una solicitud de recuperación de contraseña para el usuario.

		Args:
			user_uuid: UUID del usuario que solicita la recuperación
			expiration_hours: Horas hasta que expire el token (default: 24)

		Returns:
			RecoverPassword: La solicitud de recuperación creada
		"""
		# Generar una nueva contraseña temporal
		temporary_password = PasswordHelper.generate_password()
		hashed_password = PasswordHelper.get_password_hash(temporary_password)

		# Crear la fecha de expiración (sin timezone para coincidir con la BD)
		fecha_expiracion = datetime.now() + timedelta(hours=expiration_hours)

		# Crear el registro de recuperación
		recovery_request = RecoverPassword(
			fk_user=user_uuid,
			new_password=hashed_password,
			fecha_expiracion=fecha_expiracion,
			recovered=False,
		)

		# Guardar en el repositorio
		created_recovery = await self.auth_repository.create_recovery_password_request(
			recovery_request
		)

		# Retornar el objeto con la contraseña temporal sin hashear (solo para enviarla por email)
		created_recovery.temporary_password_plain = temporary_password
		return created_recovery


@dataclass
class CompleteRecoveryPassword(UseCase):
	auth_repository: AuthRepository
	user_service: UserServiceProtocol

	async def __call__(
		self, user_uuid: uuid.UUID, temporary_password: str, new_password: str
	) -> bool:
		"""
		Completa la recuperación de contraseña validando la contraseña temporal
		y estableciendo la nueva contraseña.

		Args:
			user_uuid: UUID del usuario
			temporary_password: Contraseña temporal enviada por email
			new_password: Nueva contraseña elegida por el usuario

		Returns:
			bool: True si se completó exitosamente

		Raises:
			ValueError: Si no hay solicitud activa o la contraseña no coincide
		"""
		from core.helpers.password import PasswordHelper

		# Buscar la solicitud de recuperación activa
		recovery_request = await self.auth_repository.get_active_recovery_request(
			user_uuid
		)

		if not recovery_request:
			raise ValueError("No hay solicitud de recuperación activa o ya expiró")

		# Validar la contraseña temporal contra el hash guardado
		is_valid = PasswordHelper.verify_password(
			temporary_password, recovery_request.new_password
		)

		if not is_valid:
			raise ValueError("Contraseña temporal inválida")

		# Obtener el usuario
		user = await self.user_service.get_user_by_uuid(str(user_uuid))
		if not user:
			raise ValueError("Usuario no encontrado")

		# Establecer la nueva contraseña
		hashed_password = PasswordHelper.get_password_hash(new_password)
		user.password = hashed_password
		user.requires_password_reset = False
		await self.user_service.save_user(user)

		# Marcar la solicitud como completada
		await self.auth_repository.mark_recovery_as_completed(recovery_request.id)  # type: ignore

		return True


@dataclass
class AuthUseCaseFactory:
	user_service: UserServiceProtocol
	auth_repository: AuthRepository

	def __post_init__(self):
		self.register_user = RegisterUser(self.user_service)
		self.get_session_user = GetSessionUser(self.auth_repository)
		self.create_recovery_password_request = CreateRecoveryPasswordRequest(
			self.auth_repository, self.user_service
		)
		self.complete_recovery_password = CompleteRecoveryPassword(
			self.auth_repository, self.user_service
		)
