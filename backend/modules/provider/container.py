from dependency_injector.providers import Container, Factory, Singleton, Provider
from dependency_injector.containers import DeclarativeContainer

from modules.provider.adapter.output.persistence.draft_invoice_adapter import DraftPurchaseInvoiceAdapter
from modules.provider.adapter.output.persistence.repository_adapter import ProviderRepositoryAdapter
from modules.provider.adapter.output.persistence.sqlalchemy.draft_purchase_invoice import DraftPurchaseInvoiceSQLAlchemyRepository
from modules.provider.adapter.output.persistence.sqlalchemy.provider import ProviderSQLAlchemyRepository
from modules.provider.application.service.draft_purchase_invoice import DraftPurchaseInvoiceService
from modules.provider.application.service.provider import ProviderService
from modules.yiqi_erp.container import YiqiContainer
from shared.container import SharedContainer
class ProviderContainer(DeclarativeContainer):

	yiqi_service = Provider()

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

	draft_invoice_repo_adapter = Factory(
		DraftPurchaseInvoiceAdapter,
		draft_purchase_invoice_repository=draft_invoice_repo
	)

	provider_service = Factory(
		ProviderService,
		provider_repository=provider_repo_adapter,
		file_storage_service=SharedContainer.file_storage.service
	)

	draft_invoice_service = Factory(
		DraftPurchaseInvoiceService,
		draft_purchase_invoice_repository=draft_invoice_repo_adapter,
		file_storage_service=SharedContainer.file_storage.service,
		yiqi_service=yiqi_service
	)