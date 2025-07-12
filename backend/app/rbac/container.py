from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer

from app.rbac.adapter.output.persistence.repository_adapter import RBACRepositoryAdapter
from app.rbac.adapter.output.persistence.sqlalchemy.rbac import RBACSQLAlchemyRepository
from app.rbac.application.service.role import RoleService
from app.rbac.application.service.permission import PermissionService

from app.module.container import AppModuleContainer
class RBACContainer(DeclarativeContainer):

	repository = Singleton(
		RBACSQLAlchemyRepository,
	)

	repository_adapter = Factory(
		RBACRepositoryAdapter,
		role_repository = repository,
		permission_repository = repository,
	)

	role_service = Factory(
		RoleService,
		role_repository=repository_adapter,
		permission_repository=repository_adapter,
		module_repository=AppModuleContainer.repository_adapter
	)

	permission_service = Factory(
		PermissionService,
		permission_repository=repository_adapter
	)