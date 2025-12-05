from celery.bin.result import result
from sqlmodel import select, delete
from typing import Sequence

from core.db import session_factory, session as global_session
from modules.provider.domain.entity.air_waybill import AirWaybill
from modules.provider.domain.repository.air_waybill import AirWaybillRepository


class AirWaybillSQLAlchemyRepository(AirWaybillRepository):
	async def get_air_waybill_by_id(self, id_air_waybill: int) -> AirWaybill | None:
		stmt = select(AirWaybill).where(AirWaybill.id == int(id_air_waybill))

		async with session_factory() as session:
			instance = await session.execute(stmt)
		return instance.scalars().one_or_none()

	async def get_air_waybills_by_draft_invoice_id(
		self, id_draft_invoice: int
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		query = select(AirWaybill).where(
			AirWaybill.fk_draft_invoice == int(id_draft_invoice)
		)
		result = await global_session.execute(query)
		return result.scalars().all()

	async def get_air_waybills_by_purchase_invoice_id(
		self, id_purchase_invoice: int
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		query = select(AirWaybill).where(
			AirWaybill.fk_purchase_invoice == int(id_purchase_invoice)
		)
		result = await global_session.execute(query)
		return result.scalars().all()

	async def validate_duplicated_air_waybill(
		self, air_waybill: AirWaybill
	) -> list[AirWaybill] | Sequence[AirWaybill]:
		query = select(AirWaybill).where(
			AirWaybill.fk_provider == air_waybill.fk_provider,
			AirWaybill.awb_code == air_waybill.awb_code,
		)
		result = await global_session.execute(query)
		return result.scalars().all()

	async def save_air_waybill(self, air_waybill: AirWaybill) -> AirWaybill:
		global_session.add(air_waybill)
		await global_session.flush()
		return air_waybill

	async def delete_air_waybill(self, air_waybill: AirWaybill):
		await global_session.delete(air_waybill)
		await global_session.flush()

	async def delete_all_air_waybills_by_draft_invoice(self, id_draft_invoice: int):
		query = delete(AirWaybill).where(
			AirWaybill.fk_draft_invoice == int(id_draft_invoice)
		)
		await global_session.execute(query)
		await global_session.flush()
