from dataclasses import dataclass
from typing import List, Sequence
from modules.finance.domain.entity.currency import Currency
from modules.finance.domain.repository.currency import CurrencyRepository


@dataclass
class CurrencyRepositoryAdapter(CurrencyRepository):
	currency_repository: CurrencyRepository

	async def get_currency_list(self) -> List[Currency] | Sequence[Currency]:
		return await self.currency_repository.get_currency_list()

	async def get_currency_by_id(self, id_currency: int) -> Currency | None:
		return await self.currency_repository.get_currency_by_id(id_currency)

	async def save(self, currency: Currency) -> Currency | None:
		return await self.currency_repository.save(currency)

	async def delete(self, currency: Currency) -> None:
		return await self.currency_repository.delete(currency)

	async def get_currency_by_code(self, currency_code: str) -> Currency | None:
		return await self.currency_repository.get_currency_by_code(currency_code)
