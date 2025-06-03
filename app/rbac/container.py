from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer

from app.rbac.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.rbac.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepository
from app.rbac.application.service.role import RoleService

class RBACContainer(DeclarativeContainer):

	repository = Singleton(
		RBACSQLAlchemyRepository,
	)

	repository_adapter = Factory(
		RBACRepositoryAdapter,
		repository=repository
	)

	service = Factory(
		RoleService,
		repository=repository_adapter
	)