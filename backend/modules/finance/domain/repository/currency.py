from abc import ABC, abstractmethod
from typing import List, Sequence

from modules.finance.domain.entity.currency import Currency


class CurrencyRepository(ABC):
	@abstractmethod
	async def get_currency_list(self) -> List[Currency] | Sequence[Currency]: ...

	@abstractmethod
	async def get_currency_by_id(self, id_currency: int) -> Currency | None: ...

	@abstractmethod
	async def get_currency_by_code(self, currency_code: str) -> Currency | None: ...

	@abstractmethod
	async def save(self, currency: Currency) -> Currency | None: ...

	@abstractmethod
	async def delete(self, currency: Currency) -> None: ...
