from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer

from app.rbac.adapter.output.persistence.repository_adapter import RBACRepositoryAdapter
from app.rbac.adapter.output.persistence.sqlalchemy.rbac import RBACSQLAlchemyRepository
from app.rbac.application.service.role import PermissionService, RoleService

class RBACContainer(DeclarativeContainer):

	repository = Singleton(
		RBACSQLAlchemyRepository,
	)

	repository_adapter = Factory(
		RBACRepositoryAdapter,
		repository=repository
	)

	role_service = Factory(
		RoleService,
		repository=repository_adapter
	)

	permission_service = Factory(
		PermissionService,
		repository=repository_adapter
	)