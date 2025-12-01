import uuid
from datetime import datetime

from sqlmodel import select

from modules.auth.domain.entity import RecoverPassword
from modules.auth.domain.repository.auth import AuthRepository
from core.db.session import session as global_session
from core.db.session import session_factory
from modules.user.application.dto import LoginResponseDTO


class AuthSQLAlchemyRepository(AuthRepository):
	"""
	Repositorio SQLAlchemy para operaciones de Auth en base de datos.
	"""

	async def create_user_session(self, login_response_dto: LoginResponseDTO):
		# Las sesiones se manejan en Redis, no en BD
		raise NotImplementedError(
			"Las sesiones se manejan en RedisAuthRepository"
		)

	async def get_user_session(self, user_uuid: str) -> LoginResponseDTO | None:
		# Las sesiones se manejan en Redis, no en BD
		raise NotImplementedError(
			"Las sesiones se manejan en RedisAuthRepository"
		)

	async def revoque_user_session(self, login_response_dto: LoginResponseDTO) -> None:
		# Las sesiones se manejan en Redis, no en BD
		raise NotImplementedError(
			"Las sesiones se manejan en RedisAuthRepository"
		)

	async def get_user_permissions(self, user_uuid: str):
		# Los permisos se manejan en Redis, no en BD
		raise NotImplementedError(
			"Los permisos se manejan en RedisAuthRepository"
		)

	async def delete_user_session(self, user_uuid: str):
		# Las sesiones se manejan en Redis, no en BD
		raise NotImplementedError(
			"Las sesiones se manejan en RedisAuthRepository"
		)

	async def create_recovery_password_request(
		self, recovery_request: RecoverPassword
	) -> RecoverPassword:
		"""
		Crea una solicitud de recuperación de contraseña en la base de datos.

		Args:
			recovery_request: La solicitud de recuperación a crear

		Returns:
			RecoverPassword: La solicitud creada con su ID
		"""
		global_session.add(recovery_request)
		await global_session.flush()
		# No hacemos refresh aquí, el @Transactional se encarga del commit
		# El ID ya está disponible porque se genera con default_factory
		return recovery_request

	async def get_active_recovery_request(
		self, user_uuid: uuid.UUID
	) -> RecoverPassword | None:
		"""
		Obtiene la solicitud de recuperación más reciente que no haya expirado
		ni haya sido completada.

		Args:
			user_uuid: UUID del usuario

		Returns:
			RecoverPassword | None: La solicitud activa o None
		"""
		now = datetime.now()

		stmt = (
			select(RecoverPassword)
			.where(RecoverPassword.fk_user == user_uuid)
			.where(RecoverPassword.recovered == False)  # noqa: E712
			.where(RecoverPassword.fecha_expiracion > now)
			.order_by(RecoverPassword.created_at.desc())
		)

		async with session_factory() as session:
			result = await session.execute(stmt)

		return result.scalars().first()

	async def mark_recovery_as_completed(self, recovery_id: uuid.UUID) -> None:
		"""
		Marca una solicitud de recuperación como completada.

		Args:
			recovery_id: UUID de la solicitud de recuperación
		"""
		stmt = select(RecoverPassword).where(RecoverPassword.id == recovery_id)

		async with session_factory() as session:
			result = await session.execute(stmt)
			recovery = result.scalars().first()

			if recovery:
				recovery.recovered = True
				session.add(recovery)
				await session.commit()
