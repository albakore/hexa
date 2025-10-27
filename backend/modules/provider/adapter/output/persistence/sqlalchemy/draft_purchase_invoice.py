from typing import Sequence
from sqlmodel import select

from core.db import session_factory, session as global_session
from modules.provider.domain.entity.draft_purchase_invoice import DraftPurchaseInvoice
from modules.provider.domain.repository.draft_purchase_invoice import (
	DraftPurchaseInvoiceRepository,
)


class DraftPurchaseInvoiceSQLAlchemyRepository(DraftPurchaseInvoiceRepository):
	async def get_provider_draft_invoices_list(
		self, id_provider: int, limit: int = 12, page: int = 0
	) -> list[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice]:
		query = select(DraftPurchaseInvoice).where(
			DraftPurchaseInvoice.fk_provider == int(id_provider)
		)
		query = query.slice(page, limit)

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
