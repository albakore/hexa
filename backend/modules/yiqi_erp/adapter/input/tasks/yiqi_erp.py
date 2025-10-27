"""
Tasks del módulo YiqiERP - Input Adapter.

Estas funciones se registrarán automáticamente como tasks de Celery
a través del service_locator y el discovery automático.
"""

from shared.interfaces.service_locator import ServiceLocator


def create_invoice_from_purchase_invoice(
	purchase_invoice_id: int, company_id: int = 316
):
	"""
	Task para crear factura en YiqiERP desde una PurchaseInvoice.

	Esta función se ejecutará de forma asíncrona a través de Celery.
	Será registrada automáticamente como: "yiqi_erp.create_invoice_from_purchase_invoice"
	"""
	service_locator = ServiceLocator()
	invoice_integration_service = service_locator.get_service(
		"yiqi_erp.invoice_integration_service"
	)
	return invoice_integration_service.create_invoice_from_purchase_invoice(
		purchase_invoice_id, company_id
	)
