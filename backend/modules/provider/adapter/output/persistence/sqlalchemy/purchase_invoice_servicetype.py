from typing import List, Sequence
from sqlmodel import col, select, delete

from core.db import session_factory, session as global_session
from core.search import DynamicSearchMixin
from modules.provider.application.dto import ProviderServiceWithRequirementsDTO
from modules.provider.domain.command import (
	LinkPurchaseInvoiceServiceToProviderCommand,
	SearchPurchaseInvoiceServiceCommand,
)
from modules.provider.domain.entity import ProviderInvoiceServiceLink
from modules.provider.domain.entity.purchase_invoice_service import (
	PurchaseInvoiceService,
)
from modules.provider.domain.repository.purchase_invoice_service import (
	PurchaseInvoiceServiceRepository,
)


class PurchaseInvoiceServiceSQLAlchemyRepository(DynamicSearchMixin, PurchaseInvoiceServiceRepository):
	model_class = PurchaseInvoiceService
	date_fields = set()  # PurchaseInvoiceService no tiene campos de fecha

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
	) -> List[ProviderServiceWithRequirementsDTO]:
		# Hacer JOIN entre PurchaseInvoiceService y ProviderInvoiceServiceLink
		query = (
			select(PurchaseInvoiceService, ProviderInvoiceServiceLink)
			.join(
				ProviderInvoiceServiceLink,
				PurchaseInvoiceService.id == ProviderInvoiceServiceLink.fk_service,
			)
			.where(col(ProviderInvoiceServiceLink.fk_provider) == int(id_provider))
		)

		async with session_factory() as session:
			result = await session.execute(query)
			rows = result.all()

		# Construir DTOs combinando datos del servicio y del link
		services_with_requirements = []
		for service, link in rows:
			dto = ProviderServiceWithRequirementsDTO(
				id=service.id,
				name=service.name,
				description=service.description,
				group=service.group,
				id_yiqi_service=service.id_yiqi_service,
				require_awb=link.require_awb,
				require_unit_price=link.require_unit_price,
				require_kg=link.require_kg,
				require_items=link.require_items,
				require_detail_file=link.require_detail_file,
			)
			services_with_requirements.append(dto)

		return services_with_requirements

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

	async def search_services(
		self, command: SearchPurchaseInvoiceServiceCommand
	) -> tuple[List[PurchaseInvoiceService] | Sequence[PurchaseInvoiceService], int]:
		"""Búsqueda dinámica de servicios de factura de compra con filtros"""
		async with session_factory() as session:
			return await self.dynamic_search(
				session=session,
				filters=command.filters,
				limit=command.limit,
				page=command.page
			)
