from typing import Sequence
from modules.provider.domain.entity.air_waybill import AirWaybill
from modules.provider.domain.repository.air_waybill import AirWaybillRepository


class AirWaybillRepositoryAdapter(AirWaybillRepository):
	def __init__(self, air_waybill_repository: AirWaybillRepository):
		self.air_waybill_repository = air_waybill_repository

	async def get_air_waybill_by_id(self, id_air_waybill: int) -> AirWaybill | None:
		return await self.air_waybill_repository.get_air_waybill_by_id(id_air_waybill)

	async def get_air_waybills_by_draft_invoice_id(
		self, id_draft_invoice: int
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		return await self.air_waybill_repository.get_air_waybills_by_draft_invoice_id(
			id_draft_invoice
		)

	async def get_air_waybills_by_purchase_invoice_id(
		self, id_purchase_invoice: int
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		return (
			await self.air_waybill_repository.get_air_waybills_by_purchase_invoice_id(
				id_purchase_invoice
			)
		)

	async def validate_duplicated_air_waybill(
		self, air_waybill: AirWaybill
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		return await self.air_waybill_repository.validate_duplicated_air_waybill(
			air_waybill
		)

	async def save_air_waybill(self, air_waybill: AirWaybill) -> AirWaybill:
		return await self.air_waybill_repository.save_air_waybill(air_waybill)

	async def delete_air_waybill(self, air_waybill: AirWaybill):
		return await self.air_waybill_repository.delete_air_waybill(air_waybill)
