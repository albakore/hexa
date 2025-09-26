from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.user.adapter.output.persistence.repository_adapter import (
	UserRepositoryAdapter,
)
from modules.user.adapter.output.persistence.sqlalchemy.user import (
	UserSQLAlchemyRepository,
)
from modules.user.application.service.user import UserService


class UserContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["modules.user"], auto_wire=True)

	repository = Singleton(
		UserSQLAlchemyRepository,
	)

	repository_adapter = Factory(UserRepositoryAdapter, repository=repository)

	service = Factory(UserService, repository=repository_adapter)
