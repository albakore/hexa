from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer

from app.module.adapter.output.persistence.repository_adapter import (
	AppModuleRepositoryAdapter,
)
from app.module.adapter.output.persistence.sqlalchemy.module import (
	AppModuleSQLAlchemyRepository,
)
from app.module.application.service.module import AppModuleService


class AppModuleContainer(DeclarativeContainer):
	repository = Singleton(AppModuleSQLAlchemyRepository)

	repository_adapter = Factory(
		AppModuleRepositoryAdapter, module_repository=repository
	)

	service = Factory(AppModuleService, app_module_repository=repository_adapter)
