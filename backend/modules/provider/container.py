from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer

from modules.provider.adapter.output.persistence.repository_adapter import ProviderRepositoryAdapter
from modules.provider.adapter.output.persistence.sqlalchemy.provider import ProviderSQLAlchemyRepository
from modules.provider.application.service.provider import ProviderService

class ProviderContainer(DeclarativeContainer):

	repository = Singleton(
		ProviderSQLAlchemyRepository,
	)

	repository_adapter = Factory(
		ProviderRepositoryAdapter,
		provider_repository=repository
	)

	service = Factory(
		ProviderService,
		provider_repository=repository_adapter
	)