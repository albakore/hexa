from typing import List, Sequence
from sqlmodel import select

from core.db import session_factory, session as global_session
from core.search import DynamicSearchMixin
from modules.provider.domain.entity.draft_purchase_invoice import DraftPurchaseInvoice
from modules.provider.domain.repository.draft_purchase_invoice import (
	DraftPurchaseInvoiceRepository,
)
from modules.provider.domain.command import SearchDraftPurchaseInvoiceCommand


class DraftPurchaseInvoiceSQLAlchemyRepository(DynamicSearchMixin, DraftPurchaseInvoiceRepository):
	model_class = DraftPurchaseInvoice
	date_fields = {"service_month", "issue_date", "receipt_date"}

	async def get_provider_draft_invoices_list(
		self, id_provider: int, limit: int = 12, page: int = 0
	) -> list[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice]:
		query = select(DraftPurchaseInvoice).where(
			DraftPurchaseInvoice.fk_provider == int(id_provider)
		)
		offset = page * limit
		query = query.offset(offset).limit(limit)

		async with session_factory() as session:
			result = await session.execute(query)

		return result.scalars().all()

	async def get_provider_draft_invoices_by_id(
		self, id_draft_purchase_invoice: int
	) -> DraftPurchaseInvoice | None:
		stmt = select(DraftPurchaseInvoice).where(
			DraftPurchaseInvoice.id == int(id_draft_purchase_invoice)
		)

		async with session_factory() as session:
			instance = await session.execute(stmt)
		return instance.scalars().one_or_none()

	async def save_draft_invoice(
		self, draft_purchase_invoice: DraftPurchaseInvoice
	) -> DraftPurchaseInvoice:
		global_session.add(draft_purchase_invoice)
		await global_session.flush()
		return draft_purchase_invoice

	async def delete_draft_invoice(self, draft_purchase_invoice: DraftPurchaseInvoice):
		await global_session.delete(draft_purchase_invoice)
		await global_session.flush()

	async def search_draft_invoices(
		self, command: SearchDraftPurchaseInvoiceCommand
	) -> tuple[List[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice], int]:
		"""Búsqueda dinámica de draft invoices con filtros"""
		async with session_factory() as session:
			return await self.dynamic_search(
				session=session,
				filters=command.filters,
				limit=command.limit,
				page=command.page
			)
