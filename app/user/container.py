from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepository
from app.user.application.service.user import UserService

class UserContainer(DeclarativeContainer):

	repository = Singleton(
		UserSQLAlchemyRepository,
	)

	repository_adapter = Factory(
		UserRepositoryAdapter,
		repository=repository
	)

	service = Factory(
		UserService,
		repository=repository_adapter
	)