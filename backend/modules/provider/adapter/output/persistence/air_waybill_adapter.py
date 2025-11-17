from typing import Sequence
from modules.provider.domain.entity.air_waybill import AirWaybill
from modules.provider.domain.repository.air_waybill import AirWaybillRepository


class AirWaybillRepositoryAdapter(AirWaybillRepository):
	def __init__(self, air_waybill_repository: AirWaybillRepository):
		self.air_waybill_repository = air_waybill_repository

	async def get_all_air_waybills(
		self, id_invoice: int, limit: int = 12, page: int = 0
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		return await self.air_waybill_repository.get_all_air_waybills(
			id_invoice, limit, page
		)

	async def get_air_waybill_by_id(self, id_air_waybill: int) -> AirWaybill | None:
		return await self.air_waybill_repository.get_air_waybill_by_id(id_air_waybill)

	async def create_air_waybill(self, air_waybill: AirWaybill) -> AirWaybill:
		return await self.air_waybill_repository.create_air_waybill(air_waybill)

	async def save_air_waybill(self, air_waybill: AirWaybill) -> AirWaybill:
		return await self.air_waybill_repository.save_air_waybill(air_waybill)

	async def delete_air_waybill(self, air_waybill: AirWaybill):
		return await self.air_waybill_repository.delete_air_waybill(air_waybill)
