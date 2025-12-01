from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Object, Singleton

from core.db.redis_db import RedisClient
from modules.auth.adapter.output.persistence.redis import RedisAuthRepository
from modules.auth.adapter.output.persistence.sqlalchemy import AuthSQLAlchemyRepository
from modules.auth.adapter.output.persistence.repository_adapter import (
	AuthRepositoryAdapter,
)
from modules.auth.application.service.auth import AuthService
from modules.auth.application.service.jwt import JwtService
from shared.interfaces.service_locator import service_locator


class AuthContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["."], auto_wire=True)

	redis_session_repository = Object(RedisClient.session)
	redis_permission_repository = Object(RedisClient.permission)

	redis_repository = Singleton(
		RedisAuthRepository,
		session_repository=redis_session_repository,
		permission_repository=redis_permission_repository,
	)

	sqlalchemy_repository = Singleton(AuthSQLAlchemyRepository)

	repository_adapter = Factory(
		AuthRepositoryAdapter,
		redis_repository=redis_repository,
		sqlalchemy_repository=sqlalchemy_repository,
	)

	service = Factory(
		AuthService,
		auth_repository=repository_adapter,
		user_service=service_locator.get_dependency("user_service"),
		role_service=service_locator.get_dependency("rbac.role_service"),
		email_template_service=service_locator.get_dependency("email_template_service"),
		notification_service=service_locator.get_dependency("notification_service"),
	)

	jwt_service = Factory(
		JwtService,
		auth_repository=repository_adapter,
		role_service=service_locator.get_dependency("rbac.role_service"),
	)
