from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from modules.rbac.adapter.output.persistence.repository_adapter import (
	RBACRepositoryAdapter,
)
from modules.rbac.adapter.output.persistence.sqlalchemy.rbac import (
	RBACSQLAlchemyRepository,
)
from modules.rbac.application.service.permission import PermissionService
from modules.rbac.application.service.role import RoleService
from shared.interfaces.service_locator import service_locator


class RBACContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["."], auto_wire=True)

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
		module_repository=service_locator.get_dependency(
			"app_module.repository_adapter"
		),
	)

	permission_service = Factory(
		PermissionService, permission_repository=repository_adapter
	)
