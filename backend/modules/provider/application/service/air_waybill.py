from dataclasses import dataclass
from typing import Sequence

from modules.provider.application.exception import (
	AirWaybillHasBeenEmittedException,
	AirWaybillNotFoundException,
	AirWaybillDuplicatedException,
)
from modules.provider.domain.command import (
	CreateAirWaybillCommand,
	UpdateAirWaybillCommand,
)
from modules.provider.domain.entity.air_waybill import AirWaybill
from modules.provider.domain.repository.air_waybill import AirWaybillRepository
from modules.provider.application.usecase.air_waybill import AirWaybillUseCaseFactory
from shared.interfaces.service_protocols.yiqi_erp import YiqiServiceProtocol


@dataclass
class AirWaybillService:
	air_waybill_repository: AirWaybillRepository
	yiqi_erp_service: YiqiServiceProtocol

	def __post_init__(self):
		self.air_waybill_usecase = AirWaybillUseCaseFactory(self.air_waybill_repository)
		self.yiqi_erp_service = self.yiqi_erp_service()

	async def get_air_waybill_by_id(self, id_air_waybill: int) -> AirWaybill:
		air_waybill = await self.air_waybill_usecase.get_air_waybill_by_id(
			id_air_waybill
		)
		if not air_waybill:
			raise AirWaybillNotFoundException
		return air_waybill

	async def get_air_waybills_by_draft_invoice_id(
		self, id_draft_invoice: int
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		return await self.air_waybill_usecase.get_air_waybills_by_draft_invoice_id(
			id_draft_invoice
		)

	async def get_air_waybills_by_purchase_invoice_id(
		self, id_purchase_invoice: int
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		air_waybills = (
			await self.air_waybill_usecase.get_air_waybills_by_purchase_invoice_id(
				id_purchase_invoice
			)
		)
		if not air_waybills:
			raise AirWaybillNotFoundException
		return air_waybills

	async def create_air_waybill(self, command: CreateAirWaybillCommand) -> AirWaybill:
		result = self.air_waybill_usecase.create_air_waybill(command)
		return result

	async def validate_duplicated_air_waybill(
		self, air_waybill: AirWaybill
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		duplicated_air_waybills = (
			await self.air_waybill_usecase.validate_duplicated_air_waybill(air_waybill)
		)
		if duplicated_air_waybills:
			raise AirWaybillDuplicatedException
		return duplicated_air_waybills

	async def update_air_waybill(
		self, id_air_waybill: int, command: UpdateAirWaybillCommand
	):
		return await self.air_waybill_usecase.update_air_waybill(
			id_air_waybill, command
		)

	async def save_air_waybill(self, air_waybill: AirWaybill) -> AirWaybill:
		if not air_waybill:
			raise AirWaybillNotFoundException
		return await self.air_waybill_usecase.save_air_waybill(air_waybill)

	async def delete_air_waybill(self, id_air_waybill: int):
		air_waybill = await self.air_waybill_usecase.get_air_waybill_by_id(
			id_air_waybill
		)
		if not air_waybill:
			raise AirWaybillNotFoundException
		if air_waybill.fk_purchase_invoice:
			raise AirWaybillHasBeenEmittedException
		return await self.air_waybill_usecase.delete_air_waybill(air_waybill)
