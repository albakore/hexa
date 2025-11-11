from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from modules.auth.container import service_locator
from modules.invoicing.adapter.output.persistence.purchase_invoice_adapter import (
	PurchaseInvoiceRepositoryAdapter,
)
from modules.invoicing.adapter.output.persistence.sqlalchemy.purchase_invoice import (
	PurchaseInvoiceSQLAlchemyRepository,
)
from modules.invoicing.application.service.purchase_invoice import (
	PurchaseInvoiceService,
)


class InvoicingContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["."], auto_wire=True)

	purchase_invoice_repo = Singleton(PurchaseInvoiceSQLAlchemyRepository)
	purchase_invoice_adapter = Factory(
		PurchaseInvoiceRepositoryAdapter, repository=purchase_invoice_repo
	)
	purchase_invoice_service = Factory(
		PurchaseInvoiceService,
		purchase_invoice_repository=purchase_invoice_adapter,
		tasks_service=service_locator.get_service("celery_app"),
	)
