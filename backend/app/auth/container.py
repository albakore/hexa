from dependency_injector.providers import Factory, Object, Singleton
from dependency_injector.containers import DeclarativeContainer

from app.auth.adapter.output.persistence.redis import RedisAuthRepository
from app.auth.adapter.output.persistence.repository_adapter import AuthRepositoryAdapter
from app.auth.application.service.auth import AuthService
from app.auth.application.service.jwt import JwtService
from app.rbac.container import RBACContainer
from modules.user.container import UserContainer
from core.db.redis_db import RedisClient


class AuthContainer(DeclarativeContainer):
	redis_session_repository = Object(RedisClient.session)
	redis_permission_repository = Object(RedisClient.permission)

	redis_repository = Singleton(
		RedisAuthRepository,
		session_repository=redis_session_repository,
		permission_repository=redis_permission_repository,
	)

	repository_adapter = Factory(AuthRepositoryAdapter, repository=redis_repository)

	service = Factory(
		AuthService,
		auth_repository=repository_adapter,
		user_repository=UserContainer.repository_adapter,
		rbac_repository=RBACContainer.repository_adapter,
	)

	jwt_service = Factory(
		JwtService,
		auth_repository=repository_adapter,
		rbac_repository=RBACContainer.repository_adapter,
	)
