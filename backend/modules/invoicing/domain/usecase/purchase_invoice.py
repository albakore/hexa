from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Sequence

from modules.invoicing.domain.entity import PurchaseInvoice
from modules.invoicing.domain.repository.purchase_invoice import (
	PurchaseInvoiceRepository,
)
from modules.invoicing.application.command import SearchPurchaseInvoiceCommand


@dataclass
class UseCase(ABC): ...


@dataclass
class GetPurchaseInvoiceList(UseCase):
	purchase_invoice_repository: PurchaseInvoiceRepository

	async def __call__(self, limit: int = 50, page: int = 0):
		return await self.purchase_invoice_repository.get_purchase_invoice_list(
			limit, page
		)


@dataclass
class GetPurchaseInvoiceListByProvider(UseCase):
	purchase_invoice_repository: PurchaseInvoiceRepository

	async def __call__(self, id_provider: int, limit: int = 50, page: int = 0):
		return await self.purchase_invoice_repository.get_purchase_invoice_list_by_provider(
			id_provider, limit, page
		)


@dataclass
class GetPurchaseInvoiceById(UseCase):
	purchase_invoice_repository: PurchaseInvoiceRepository

	async def __call__(self, id_purchase_invoice: int):
		return await self.purchase_invoice_repository.get_purchase_invoice_by_id(
			id_purchase_invoice
		)


@dataclass
class SavePurchaseInvoice(UseCase):
	purchase_invoice_repository: PurchaseInvoiceRepository

	async def __call__(self, purchase_invoice: PurchaseInvoice) -> PurchaseInvoice:
		return await self.purchase_invoice_repository.save_purchase_invoice(
			purchase_invoice
		)


@dataclass
class SearchPurchaseInvoicesUseCase(UseCase):
	purchase_invoice_repository: PurchaseInvoiceRepository

	async def __call__(
		self, command: SearchPurchaseInvoiceCommand
	) -> tuple[List[PurchaseInvoice] | Sequence[PurchaseInvoice], int]:
		return await self.purchase_invoice_repository.search_purchase_invoices(command)


@dataclass
class InvoiceUseCaseFactory:
	purchase_invoice_repository: PurchaseInvoiceRepository

	def __post_init__(self):
		self.get_purchase_invoice_list = GetPurchaseInvoiceList(
			self.purchase_invoice_repository
		)
		self.get_purchase_invoice_list_by_provider = GetPurchaseInvoiceListByProvider(
			self.purchase_invoice_repository
		)
		self.get_purchase_invoice_by_id = GetPurchaseInvoiceById(
			self.purchase_invoice_repository
		)
		self.save_purchase_invoice = SavePurchaseInvoice(
			self.purchase_invoice_repository
		)
		self.search_purchase_invoices = SearchPurchaseInvoicesUseCase(
			self.purchase_invoice_repository
		)
