from typing import Sequence
from sqlmodel import select

from core.db import session_factory, session as global_session
from modules.provider.domain.entity.air_waybill import AirWaybill
from modules.provider.domain.repository.air_waybill import AirWaybillRepository


class AirWaybillSQLAlchemyRepository(AirWaybillRepository):
	async def get_all_air_waybills(
		self, id_invoice: int, limit: int = 12, page: int = 0
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		query = select(AirWaybill).where(AirWaybill.fk_draft_invoice == int(id_invoice))
		offset = page * limit
		query = query.offset(offset).limit(limit)

		result = await global_session.execute(query)

		return result.scalars().all()

	async def get_air_waybill_by_id(self, id: int) -> AirWaybill | None:
		stmt = select(AirWaybill).where(AirWaybill.id == int(id))

		async with session_factory() as session:
			instance = await session.execute(stmt)
		return instance.scalars().one_or_none()

	async def save_air_waybill(self, air_waybill: AirWaybill) -> AirWaybill:
		global_session.add(air_waybill)
		await global_session.flush()
		return air_waybill

	async def delete_air_waybill(self, air_waybill: AirWaybill):
		await global_session.delete(air_waybill)
		await global_session.flush()

	async def create_air_waybill(self, air_waybill):
		raise NotImplementedError
