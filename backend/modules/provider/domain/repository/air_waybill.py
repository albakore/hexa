from typing import Sequence
from modules.provider.domain.entity.air_waybill import AirWaybill
from abc import ABC, abstractmethod


class AirWaybillRepository(ABC):
	@abstractmethod
	async def get_air_waybill_by_id(self, id_air_waybill: int) -> AirWaybill | None: ...

	@abstractmethod
	async def get_air_waybills_by_draft_invoice_id(
		self, id_draft_invoice: int
	) -> list[AirWaybill] | Sequence[AirWaybill]: ...

	@abstractmethod
	async def get_air_waybills_by_purchase_invoice_id(
		self, id_purchase_invoice: int
	) -> list[AirWaybill] | Sequence[AirWaybill]: ...

	@abstractmethod
	async def validate_duplicated_air_waybill(
		self, air_waybill: AirWaybill
	) -> list[AirWaybill] | Sequence[AirWaybill]: ...

	@abstractmethod
	async def save_air_waybill(self, air_waybill: AirWaybill) -> AirWaybill: ...

	@abstractmethod
	async def delete_air_waybill(self, air_waybill: AirWaybill): ...
