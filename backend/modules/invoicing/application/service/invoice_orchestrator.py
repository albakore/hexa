from dataclasses import dataclass
from shared.interfaces.service_locator import ServiceLocator
from shared.interfaces.service_protocols import (
	PurchaseInvoiceServiceProtocol,
	DraftPurchaseInvoiceServiceProtocol,
)
from modules.invoicing.application.command import CreatePurchaseInvoiceCommand


@dataclass
class InvoiceOrchestratorService:
	purchase_invoice_service: PurchaseInvoiceServiceProtocol

	async def create_invoice_from_draft(self, draft_purchase_invoice_id: int):
		"""
		Crea una PurchaseInvoice desde un DraftPurchaseInvoice y envía task a YiqiERP.
		"""
		service_locator = ServiceLocator()
		draft_service: DraftPurchaseInvoiceServiceProtocol = (
			service_locator.get_service("provider.draft_invoice_service")
		)

		# Obtener draft
		draft = await draft_service.get_draft_purchase_invoice_by_id(
			draft_purchase_invoice_id
		)

		# Crear comando para PurchaseInvoice
		purchase_invoice_command = CreatePurchaseInvoiceCommand(
			fk_provider=draft.fk_provider,
			fk_service=draft.fk_invoice_service,
			number=draft.number,
			concept=draft.concept or "Sin concepto agregado",
			issue_date=draft.issue_date,
			receipt_date=draft.receipt_date,
			service_month=draft.service_month,
			period_from_date=None,
			period_until_date=None,
			currency=draft.currency,
			unit_price=draft.unit_price or 0.0,
			air_waybill=draft.awb,
			kilograms=draft.kg,
			items=draft.items,
			fk_receipt_file=draft.id_receipt_file,
			fk_detail_file=draft.id_details_file,
		)

		# Crear y guardar PurchaseInvoice
		purchase_invoice = await self.purchase_invoice_service.create(
			purchase_invoice_command
		)
		saved_invoice = await self.purchase_invoice_service.save(purchase_invoice)

		# Enviar task a YiqiERP
		celery_app = service_locator.get_service("celery_app")
		celery_app.send_task(
			"yiqi_erp.create_invoice_from_purchase_invoice", args=[saved_invoice.id]
		)

		# Actualizar estado del draft
		draft.state = "Created"
		draft.fk_invoice = saved_invoice.id
		await draft_service.save_draft_purchase_invoice(draft)

		return saved_invoice
