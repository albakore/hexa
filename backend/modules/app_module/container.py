from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.app_module.adapter.output.persistence.repository_adapter import (
	AppModuleRepositoryAdapter,
)
from modules.app_module.adapter.output.persistence.sqlalchemy.module import (
	AppModuleSQLAlchemyRepository,
)
from modules.app_module.application.service.module import AppModuleService


class AppModuleContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["modules.app_module"], auto_wire=True)

	repository = Singleton(AppModuleSQLAlchemyRepository)

	repository_adapter = Factory(
		AppModuleRepositoryAdapter, module_repository=repository
	)

	service = Factory(AppModuleService, app_module_repository=repository_adapter)
