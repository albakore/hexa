from dependency_injector.providers import Container, Factory, Singleton, Provider
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from modules.provider.adapter.output.persistence.air_waybill_adapter import (
	AirWaybillRepositoryAdapter,
)
from modules.provider.adapter.output.persistence.sqlalchemy.air_waybill import (
	AirWaybillSQLAlchemyRepository,
)
from modules.provider.application.service.air_waybill import AirWaybillService
from shared.interfaces.service_locator import service_locator
from modules.provider.adapter.output.persistence.draft_invoice_adapter import (
	DraftPurchaseInvoiceAdapter,
)
from modules.provider.adapter.output.persistence.invoice_service_adapter import (
	PurchaseInvoiceServiceRepositoryAdapter,
)
from modules.provider.adapter.output.persistence.repository_adapter import (
	ProviderRepositoryAdapter,
)
from modules.provider.adapter.output.persistence.sqlalchemy.draft_purchase_invoice import (
	DraftPurchaseInvoiceSQLAlchemyRepository,
)
from modules.provider.adapter.output.persistence.sqlalchemy.provider import (
	ProviderSQLAlchemyRepository,
)
from modules.provider.adapter.output.persistence.sqlalchemy.purchase_invoice_servicetype import (
	PurchaseInvoiceServiceSQLAlchemyRepository,
)
from modules.provider.application.service.draft_purchase_invoice import (
	DraftPurchaseInvoiceService,
)
from modules.provider.application.service.provider import ProviderService
from modules.provider.application.service.purchase_invoice_service import (
	PurchaseInvoiceServiceTypeService,
)


class ProviderContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["."], auto_wire=True)

	provider_repo = Singleton(
		ProviderSQLAlchemyRepository,
	)

	draft_invoice_repo = Singleton(DraftPurchaseInvoiceSQLAlchemyRepository)

	invoice_service_repo = Singleton(PurchaseInvoiceServiceSQLAlchemyRepository)

	air_waybill_repo = Singleton(AirWaybillSQLAlchemyRepository)

	provider_repo_adapter = Factory(
		ProviderRepositoryAdapter, provider_repository=provider_repo
	)

	draft_invoice_repo_adapter = Factory(
		DraftPurchaseInvoiceAdapter,
		draft_purchase_invoice_repository=draft_invoice_repo,
	)

	invoice_service_repo_adapter = Factory(
		PurchaseInvoiceServiceRepositoryAdapter,
		purchase_invoice_service_repository=invoice_service_repo,
	)

	air_waybill_repo_adapter = Factory(
		AirWaybillRepositoryAdapter, air_waybill_repository=air_waybill_repo
	)

	provider_service = Factory(
		ProviderService,
		provider_repository=provider_repo_adapter,
		# file_storage_service=SharedContainer.file_storage.service
	)

	invoice_servicetype_service = Factory(
		PurchaseInvoiceServiceTypeService,
		purchase_invoice_service_repository=invoice_service_repo_adapter,
	)

	air_waybill_service = Factory(
		AirWaybillService,
		air_waybill_repository=air_waybill_repo_adapter,
		yiqi_erp_service=service_locator.get_dependency("yiqi_service"),
	)

	draft_invoice_service = Factory(
		DraftPurchaseInvoiceService,
		draft_purchase_invoice_repository=draft_invoice_repo_adapter,
		draft_purchase_invoice_servicetype_service=invoice_servicetype_service,
		purchase_invoice_service=service_locator.get_dependency(
			"purchase_invoice_service"
		),
		file_storage_service=service_locator.get_dependency("file_storage_service"),
		currency_service=service_locator.get_dependency("currency_service"),
		air_waybill_service=air_waybill_service,
	)
