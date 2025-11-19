from dataclasses import dataclass
from typing import List, Sequence

from core.db import Transactional
from modules.provider.application.dto import ProviderServiceWithRequirementsDTO
from modules.provider.domain.command import (
	CreatePurchaseInvoiceServiceCommand,
	LinkPurchaseInvoiceServiceToProviderCommand,
	UpdatePurchaseInvoiceServiceCommand,
)
from modules.provider.domain.entity.purchase_invoice_service import (
	PurchaseInvoiceService,
	ProviderInvoiceServiceLink,
)
from modules.provider.domain.exception import (
	DraftPurchaseInvoiceServiceNotFoundException,
)
from modules.provider.domain.repository.purchase_invoice_service import (
	PurchaseInvoiceServiceRepository,
)


@dataclass
class GetProviderInvoicesListUseCase:
	purchase_invoice_repository: PurchaseInvoiceServiceRepository

	async def __call__(
		self, limit: int = 50, page: int = 0
	) -> list[PurchaseInvoiceService] | Sequence[PurchaseInvoiceService]:
		return await self.purchase_invoice_repository.get_services_list(limit, page)


@dataclass
class GetPurchaseInvoiceServicesByIdUseCase:
	purchase_invoice_repository: PurchaseInvoiceServiceRepository

	async def __call__(self, id_purchase_invoice: int) -> PurchaseInvoiceService | None:
		return await self.purchase_invoice_repository.get_services_by_id(
			id_purchase_invoice
		)


@dataclass
class CreatePurchaseInvoiceServiceUseCase:
	def __call__(
		self, command: CreatePurchaseInvoiceServiceCommand
	) -> PurchaseInvoiceService:
		return PurchaseInvoiceService.model_validate(command)


@dataclass
class UpdatePurchaseInvoiceServiceUseCase:
	purchase_invoice_repository: PurchaseInvoiceServiceRepository

	@Transactional()
	async def __call__(self, command: UpdatePurchaseInvoiceServiceCommand):
		service = await self.purchase_invoice_repository.get_services_by_id(command.id)
		if not service:
			raise DraftPurchaseInvoiceServiceNotFoundException
		service.sqlmodel_update(command)
		return await self.purchase_invoice_repository.save_service(service)


@dataclass
class SavePurchaseInvoiceServicesUseCase:
	purchase_invoice_repository: PurchaseInvoiceServiceRepository

	@Transactional()
	async def __call__(
		self, purchase_invoice: PurchaseInvoiceService
	) -> PurchaseInvoiceService | None:
		return await self.purchase_invoice_repository.save_service(purchase_invoice)


@dataclass
class DeletePurchaseInvoiceServicesUseCase:
	purchase_invoice_repository: PurchaseInvoiceServiceRepository

	@Transactional()
	async def __call__(self, purchase_invoice: PurchaseInvoiceService) -> None:
		return await self.purchase_invoice_repository.delete_service(purchase_invoice)


@dataclass
class GetServicesOfProviderUseCase:
	purchase_invoice_repository: PurchaseInvoiceServiceRepository

	async def __call__(self, id_provider: int) -> List[ProviderServiceWithRequirementsDTO]:
		return await self.purchase_invoice_repository.get_services_of_provider(
			id_provider
		)


@dataclass
class AddServicesToProviderUseCase:
	purchase_invoice_repository: PurchaseInvoiceServiceRepository

	@Transactional()
	async def __call__(
		self,
		id_provider: int,
		services: List[LinkPurchaseInvoiceServiceToProviderCommand],
	):
		return await self.purchase_invoice_repository.add_services_to_provider(
			id_provider, services
		)


@dataclass
class RemoveServicesFromProviderUseCase:
	purchase_invoice_repository: PurchaseInvoiceServiceRepository

	@Transactional()
	async def __call__(self, id_provider: int, id_services_list: List[int]):
		return await self.purchase_invoice_repository.remove_services_from_provider(
			id_provider, id_services_list
		)


@dataclass
class GetProviderServiceLinkUseCase:
	purchase_invoice_repository: PurchaseInvoiceServiceRepository

	async def __call__(
		self, id_provider: int, id_service: int
	) -> ProviderInvoiceServiceLink | None:
		return await self.purchase_invoice_repository.get_provider_service_link(
			id_provider, id_service
		)


@dataclass
class PurchaseInvoiceServiceUseCaseFactory:
	purchase_invoice_repository: PurchaseInvoiceServiceRepository

	def __post_init__(self):
		self.get_services_list = GetProviderInvoicesListUseCase(
			self.purchase_invoice_repository
		)
		self.get_service_by_id = GetPurchaseInvoiceServicesByIdUseCase(
			self.purchase_invoice_repository
		)
		self.create_invoice_service = CreatePurchaseInvoiceServiceUseCase()
		self.update_invoice_service = UpdatePurchaseInvoiceServiceUseCase(
			self.purchase_invoice_repository
		)
		self.save_purchase_invoice = SavePurchaseInvoiceServicesUseCase(
			self.purchase_invoice_repository
		)
		self.delete_invoice_service = DeletePurchaseInvoiceServicesUseCase(
			self.purchase_invoice_repository
		)
		self.get_services_of_provider = GetServicesOfProviderUseCase(
			self.purchase_invoice_repository
		)
		self.add_services_to_provider = AddServicesToProviderUseCase(
			self.purchase_invoice_repository
		)
		self.remove_services_from_provider = RemoveServicesFromProviderUseCase(
			self.purchase_invoice_repository
		)
		self.get_provider_service_link = GetProviderServiceLinkUseCase(
			self.purchase_invoice_repository
		)
