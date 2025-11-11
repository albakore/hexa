from dataclasses import dataclass
from typing import List, Sequence

from sqlmodel import select

from core.db import session_factory, session as global_session
from modules.finance.domain.entity.currency import Currency
from modules.finance.domain.repository.currency import CurrencyRepository


@dataclass
class CurrencySQLAlchemyRepository(CurrencyRepository):
	async def get_currency_list(self) -> List[Currency] | Sequence[Currency]:
		stmt = select(Currency)
		async with session_factory() as session:
			result = await session.execute(stmt)
			currencies = result.scalars().all()

		return currencies

	async def get_currency_by_id(self, id_currency: int) -> Currency | None:
		currency = await global_session.get(Currency, int(id_currency))
		return currency

	async def save(self, currency: Currency) -> Currency | None:
		global_session.add(currency)
		await global_session.flush()
		return currency

	async def delete(self, currency: Currency) -> None:
		await global_session.delete(currency)

	async def get_currency_by_code(self, currency_code: str) -> Currency | None:
		stmt = select(Currency).where(Currency.code == str(currency_code))
		async with session_factory() as session:
			result = await session.execute(stmt)
			currency = result.scalars().one_or_none()

		return currency
