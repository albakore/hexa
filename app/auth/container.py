from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import provided

from app.auth.adapter.output.persistence.redis import RedisAuthRepository
from app.auth.adapter.output.persistence.repository_adapter import AuthRepositoryAdapter
from app.auth.application.service.auth import AuthService
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepository
from app.user.container import UserContainer

class AuthContainer(DeclarativeContainer):

	repository = Singleton(
		RedisAuthRepository,
	)

	repository_adapter = Factory(
		AuthRepositoryAdapter,
		repository=repository
	)

	service = Factory(
		AuthService,
		db_repository=repository_adapter,
		user_repository=UserContainer.repository_adapter
	)
