from dataclasses import dataclass
from typing import Sequence

from core.db.transactional import Transactional
from modules.invoicing.domain.repository.purchase_invoice import (
	PurchaseInvoiceRepository,
)
from modules.provider.domain.command import (
	CreateAirWaybillCommand,
	UpdateAirWaybillCommand,
)
from modules.provider.domain.entity.air_waybill import AirWaybill
from modules.provider.domain.exception import AirWaybillNotFoundException
from modules.provider.domain.repository.air_waybill import AirWaybillRepository


@dataclass
class GetAllAirWaybillsUseCase:
	air_waybill_repository: AirWaybillRepository

	async def __call__(
		self, id_invoice, limit: int = 20, page: int = 0
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		return await self.air_waybill_repository.get_all_air_waybills(
			id_invoice, limit, page
		)


@dataclass
class GetAirWaybillByIdUseCase:
	air_waybill_repository: AirWaybillRepository

	async def __call__(self, id_air_waybill: int) -> AirWaybill | None:
		return await self.air_waybill_repository.get_air_waybill_by_id(id_air_waybill)


@dataclass
class CreateAirWaybillUseCase:
	air_waybill_repository: AirWaybillRepository

	def __call__(self, command: CreateAirWaybillCommand) -> AirWaybill:
		return AirWaybill.model_validate(command)


@dataclass
class SaveAirWaybillUseCase:
	air_waybill_repository: AirWaybillRepository

	@Transactional()
	async def __call__(self, air_waybill: AirWaybill) -> AirWaybill:
		return await self.air_waybill_repository.save_air_waybill(air_waybill)


@dataclass
class UpdateAirWaybillUseCase:
	air_waybill_repository: AirWaybillRepository

	@Transactional()
	async def __call__(self, command: UpdateAirWaybillCommand):
		air_waybill = await self.air_waybill_repository.get_air_waybill_by_id(
			command.id
		)
		if not air_waybill:
			raise AirWaybillNotFoundException
		air_waybill.sqlmodel_update(command.model_dump(exclude_unset=True))
		return await self.air_waybill_repository.save_air_waybill(air_waybill)


@dataclass
class DeleteAirWaybillUseCase:
	air_waybill_repository: AirWaybillRepository

	@Transactional()
	async def __call__(self, air_waybill: AirWaybill):
		return await self.air_waybill_repository.delete_air_waybill(air_waybill)


@dataclass
class LinkInvoiceToAirWaybillUseCase:
	air_waybill_repository: AirWaybillRepository
	invoice_repository: PurchaseInvoiceRepository

	@Transactional()
	async def __call__(self, air_waybill: AirWaybill, invoice_id: int):
		invoice = await self.invoice_repository.get_purchase_invoice_by_id(invoice_id)
		if not invoice:
			raise AirWaybillNotFoundException
		return await self.air_waybill_repository.save_air_waybill(air_waybill)


@dataclass
class AirWaybillUseCaseFactory:
	air_waybill_repository: AirWaybillRepository

	def __post_init__(self):
		self.get_air_waybills = GetAllAirWaybillsUseCase(self.air_waybill_repository)
		self.get_air_waybill_by_id = GetAirWaybillByIdUseCase(
			self.air_waybill_repository
		)
		self.create_air_waybill = CreateAirWaybillUseCase(self.air_waybill_repository)
		self.save_air_waybill = SaveAirWaybillUseCase(self.air_waybill_repository)
		self.update_air_waybill = UpdateAirWaybillUseCase(self.air_waybill_repository)
		self.delete_air_waybill = DeleteAirWaybillUseCase(self.air_waybill_repository)
