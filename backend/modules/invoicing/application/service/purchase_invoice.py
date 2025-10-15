from dataclasses import dataclass

from modules.invoicing.application.command import CreatePurchaseInvoiceCommand
from modules.invoicing.application.dto import PurchaseInvoiceDTO
from modules.invoicing.domain.repository.purchase_invoice import (
	PurchaseInvoiceRepository,
)


@dataclass
class PurchaseInvoiceService:
	purchase_invoice_repository: PurchaseInvoiceRepository

	async def get_list(self, limit: int, page: int): ...
	async def get_one_by_id(self, id_purchase_invoice: int): ...
	async def create(self, command: CreatePurchaseInvoiceCommand): ...
	async def save(self, purchase_invoice_dto: PurchaseInvoiceDTO): ...
