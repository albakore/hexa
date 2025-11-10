from dataclasses import dataclass
from typing import Sequence

from modules.provider.domain.entity.air_waybill import AirWaybill
from modules.provider.domain.repository.air_waybill import AirWaybillRepository
from modules.provider.domain.usecase.air_waybill import GetAirWaybillsUseCase


@dataclass
class AirWaybillService:
	air_waybill_repository: AirWaybillRepository

	def __post_init__(self):
		self.get_air_waybills_usecase = GetAirWaybillsUseCase(
			self.air_waybill_repository
		)

	async def get_all_air_waybills(
		self, limit: int = 20, page: int = 0
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		return await self.get_air_waybills_usecase(limit, page)

	async def get_air_waybill_by_id(
		self, id_air_waybill: int
	) -> AirWaybill | None:
		air_waybill = await self.air_waybill_repository.get_air_waybill_by_id(id_air_waybill)
		if not air_waybill:
			raise Exception("AirWaybill not found")
			# raise AirWaybillNotFoundException  # Uncomment and define this exception if needed
		return air_waybill
	