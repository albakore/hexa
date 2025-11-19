from typing import List, Sequence
from sqlmodel import col, select, delete

from core.db import session_factory, session as global_session
from modules.provider.domain.command import LinkPurchaseInvoiceServiceToProviderCommand
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
		offset = page * limit
		query = query.offset(offset).limit(limit)

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
		self, id_provider: int, services: List[LinkPurchaseInvoiceServiceToProviderCommand]
	) -> None:
		# Crear diccionario para mapear id del servicio con el comando completo
		services_dict = {service.id: service for service in services}

		query_services = select(PurchaseInvoiceService).where(
			col(PurchaseInvoiceService.id).in_([service.id for service in services])
		)

		services_result = await global_session.execute(query_services)
		services_from_db = services_result.scalars().all()

		service_links = []
		for service in services_from_db:
			if service.id is not None and service.id in services_dict:
				service_command = services_dict[service.id]
				service_links.append(
					ProviderInvoiceServiceLink(
						fk_provider=int(id_provider),
						fk_service=service.id,
						require_awb=service_command.require_awb,
						require_unit_price=service_command.require_unit_price,
						require_kg=service_command.require_kg,
						require_items=service_command.require_items,
						require_detail_file=service_command.require_detail_file,
					)
				)

		global_session.add_all(service_links)

	async def remove_services_from_provider(
		self, id_provider: int, id_services_list: List[int]
	) -> None:
		query_remove_services = (
			delete(ProviderInvoiceServiceLink)
			.where(col(ProviderInvoiceServiceLink.fk_provider) == int(id_provider))
			.where(col(ProviderInvoiceServiceLink.fk_service).in_(id_services_list))
		)

		await global_session.execute(query_remove_services)

	async def get_provider_service_link(
		self, id_provider: int, id_service: int
	) -> ProviderInvoiceServiceLink | None:
		query = select(ProviderInvoiceServiceLink).where(
			col(ProviderInvoiceServiceLink.fk_provider) == int(id_provider),
			col(ProviderInvoiceServiceLink.fk_service) == int(id_service),
		)

		async with session_factory() as session:
			result = await session.execute(query)

		return result.scalar_one_or_none()
