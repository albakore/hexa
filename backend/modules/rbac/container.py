from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from backend.shared.dependencies import service_locator
from modules.rbac.adapter.output.persistence.repository_adapter import (
	RBACRepositoryAdapter,
)
from modules.rbac.adapter.output.persistence.sqlalchemy.rbac import (
	RBACSQLAlchemyRepository,
)
from modules.rbac.application.service.role import RoleService
from modules.rbac.application.service.permission import PermissionService


class RBACContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["modules.rbac"], auto_wire=True)

	repository = Singleton(
		RBACSQLAlchemyRepository,
	)

	repository_adapter = Factory(
		RBACRepositoryAdapter,
		role_repository=repository,
		permission_repository=repository,
	)

	role_service = Factory(
		RoleService,
		role_repository=repository_adapter,
		permission_repository=repository_adapter,
	)

	permission_service = Factory(
		PermissionService, permission_repository=repository_adapter
	)


service_locator.register_service("role_service", RBACContainer.role_service)
service_locator.register_service("permission_service", RBACContainer.permission_service)
