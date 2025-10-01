from typing import List, Sequence
from sqlmodel import col, select, delete

from core.db import session_factory, session as global_session
from modules.provider.domain.entity import ProviderInvoiceServiceLink
from modules.provider.domain.entity.purchase_invoice_service import (
	PurchaseInvoiceService,
)
from modules.provider.domain.repository.purchase_invoice_service import (
	PurchaseInvoiceServiceRepository,
)


class PurchaseInvoiceServiceSQLAlchemyRepository(PurchaseInvoiceServiceRepository):
	async def get_services_list(
		self, limit: int = 12, page: int = 0
	) -> List[PurchaseInvoiceService] | Sequence[PurchaseInvoiceService]:
		query = select(PurchaseInvoiceService)
		query = query.slice(page, limit)

		async with session_factory() as session:
			result = await session.execute(query)

		return result.scalars().all()

	async def get_services_by_id(
		self, id_service: int
	) -> PurchaseInvoiceService | None:
		async with session_factory() as session:
			result = await session.get(PurchaseInvoiceService, int(id_service))

		return result

	async def save_service(
		self, invoice_service: PurchaseInvoiceService
	) -> PurchaseInvoiceService | None:
		global_session.add(invoice_service)
		await global_session.flush()
		return invoice_service

	async def delete_service(self, invoice_service: PurchaseInvoiceService):
		await global_session.delete(invoice_service)
		await global_session.flush()

	async def get_services_of_provider(
		self, id_provider: int
	) -> List[PurchaseInvoiceService] | Sequence[PurchaseInvoiceService]:
		query_id_list_services = select(ProviderInvoiceServiceLink.fk_service).where(
			ProviderInvoiceServiceLink.fk_provider == int(id_provider)
		)

		query_services = select(PurchaseInvoiceService).where(
			col(PurchaseInvoiceService.id).in_(query_id_list_services)
		)

		async with session_factory() as session:
			result = await session.execute(query_services)

		return result.scalars().all()

	async def add_services_to_provider(
		self, id_provider: int, id_services_list: List[int]
	) -> None:
		query_services = select(PurchaseInvoiceService).where(
			col(PurchaseInvoiceService.id).in_(id_services_list)
		)

		services_result = await global_session.execute(query_services)
		services = services_result.scalars().all()

		global_session.add_all(
			[
				ProviderInvoiceServiceLink(
					fk_provider=int(id_provider), fk_service=service.id
				)
				for service in services
			]
		)

	async def remove_services_from_provider(
		self, id_provider: int, id_services_list: List[int]
	) -> None:
		query_remove_services = (
			delete(ProviderInvoiceServiceLink)
			.where(ProviderInvoiceServiceLink.fk_provider == int(id_provider))
			.where(col(ProviderInvoiceServiceLink.fk_service).in_(id_services_list))
		)

		await global_session.execute(query_remove_services)
