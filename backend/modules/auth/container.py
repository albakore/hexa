from dependency_injector.providers import Factory, Object, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.auth.adapter.output.persistence.redis import RedisAuthRepository
from modules.auth.adapter.output.persistence.repository_adapter import (
	AuthRepositoryAdapter,
)
from modules.auth.application.service.auth import AuthService
from modules.auth.application.service.jwt import JwtService
from core.db.redis_db import RedisClient


class AuthContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["modules.auth"], auto_wire=True)

	redis_session_repository = Object(RedisClient.session)
	redis_permission_repository = Object(RedisClient.permission)

	redis_repository = Singleton(
		RedisAuthRepository,
		session_repository=redis_session_repository,
		permission_repository=redis_permission_repository,
	)

	repository_adapter = Factory(AuthRepositoryAdapter, repository=redis_repository)

	# Simplified services without complex dependencies for now
	# Dependencies will be injected at endpoint level
	auth_service_simple = Factory(
		AuthService,
		auth_repository=repository_adapter,
		user_repository=repository_adapter,  # Temporary
		rbac_repository=repository_adapter,  # Temporary
	)

	jwt_service = Factory(
		JwtService,
		auth_repository=repository_adapter,
		rbac_repository=repository_adapter,  # Temporary
	)