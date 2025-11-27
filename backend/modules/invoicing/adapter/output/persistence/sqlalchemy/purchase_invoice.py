from typing import List, Sequence

from sqlmodel import select

from core.db import session as global_session
from core.db import session_factory
from core.search import DynamicSearchMixin
from modules.invoicing.application.command import SearchPurchaseInvoiceCommand
from modules.invoicing.domain.entity import PurchaseInvoice
from modules.invoicing.domain.repository.purchase_invoice import (
	PurchaseInvoiceRepository,
)


class PurchaseInvoiceSQLAlchemyRepository(
	DynamicSearchMixin, PurchaseInvoiceRepository
):
	model_class = PurchaseInvoice
	date_fields = {
		"service_month",
		"issue_date",
		"receipt_date",
		"period_from_date",
		"period_until_date",
	}

	async def get_purchase_invoice_by_id(self, id_purchase_invoice: int):
		query = select(PurchaseInvoice).where(
			PurchaseInvoice.id == int(id_purchase_invoice)
		)
		result = await global_session.execute(query)

		return result.scalars().first()

	async def get_purchase_invoice_list(self, limit: int, page: int):
		query = select(PurchaseInvoice)
		offset = page * limit
		query = query.offset(offset).limit(limit)

		async with session_factory() as session:
			result = await session.execute(query)

		return result.scalars().all()

	async def save_purchase_invoice(self, purchase_invoice: PurchaseInvoice):
		global_session.add(purchase_invoice)
		await global_session.flush()
		return purchase_invoice

	async def get_purchase_invoice_list_by_provider(
		self, id_provider: int, limit: int, page: int
	):
		query = select(PurchaseInvoice).where(
			PurchaseInvoice.fk_provider == int(id_provider)
		)
		offset = page * limit
		query = query.offset(offset).limit(limit)

		async with session_factory() as session:
			result = await session.execute(query)

		return result.scalars().all()

	async def search_purchase_invoices(
		self, command: SearchPurchaseInvoiceCommand
	) -> tuple[List[PurchaseInvoice] | Sequence[PurchaseInvoice], int]:
		"""Búsqueda dinámica de purchase invoices con filtros"""
		async with session_factory() as session:
			return await self.dynamic_search(
				session=session,
				filters=command.filters,
				limit=command.limit,
				page=command.page,
				model_class=self.model_class,
			)
