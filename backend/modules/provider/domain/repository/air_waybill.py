from typing import Sequence
from modules.provider.domain.entity.air_waybill import AirWaybill
from abc import ABC, abstractmethod


class AirWaybillRepository(ABC):
	@abstractmethod
	async def get_all_air_waybills(
		self, limit: int = 12, page: int = 0
	) -> list[AirWaybill] | Sequence[AirWaybill]: ...

	@abstractmethod
	async def get_air_waybill_by_id(self, id_air_waybill: int) -> AirWaybill | None: ...

	@abstractmethod
	async def save(self, air_waybill: AirWaybill) -> AirWaybill | None: ...

	@abstractmethod
	async def delete(self, air_waybill: AirWaybill): ...
