from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer

from modules.provider.adapter.output.persistence.repository_adapter import ProviderRepositoryAdapter
from modules.provider.adapter.output.persistence.sqlalchemy.draft_purchase_invoice import DraftPurchaseInvoiceSQLAlchemyRepository
from modules.provider.adapter.output.persistence.sqlalchemy.provider import ProviderSQLAlchemyRepository
from modules.provider.application.service.draft_purchase_invoice import DraftPurchaseInvoiceService
from modules.provider.application.service.provider import ProviderService
from shared.container import SharedContainer
class ProviderContainer(DeclarativeContainer):

	provider_repo = Singleton(
		ProviderSQLAlchemyRepository,
	)

	draft_invoice_repo = Singleton(
		DraftPurchaseInvoiceSQLAlchemyRepository
	)

	provider_repo_adapter = Factory(
		ProviderRepositoryAdapter,
		provider_repository=provider_repo
	)

	#TODO: Agregar el adaptador de draft invoice

	# draft_invoice_repo_adapter = Factory(
	# 	DraftPurchaseInvoiceSQLAlchemyRepository,
	# 	provider_repository=provider_repo
	# )

	provider_service = Factory(
		ProviderService,
		provider_repository=provider_repo_adapter,
		file_storage_service=SharedContainer.file_storage.service
	)

	#TODO: Agregar el adaptador de draft invoice al servicio

	# draft_invoice_service = Factory(
	# 	DraftPurchaseInvoiceService,
	# 	draft_purchase_invoice_repository=DraftPurchaseInvoiceRepository,
	# 	file_storage_service=SharedContainer.file_storage.service
	# )