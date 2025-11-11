from dataclasses import dataclass

from modules.finance.application.exception.currency import (
	CurrencyDuplicationException,
	CurrencyNotFoundException,
)
from modules.finance.domain.command.currency import (
	CreateCurrencyCommand,
	UpdateCurrencyCommand,
)
from modules.finance.domain.entity.currency import Currency
from modules.finance.domain.repository.currency import CurrencyRepository
from modules.finance.domain.usecase.currency import CurrencyUseCaseFactory


@dataclass
class CurrencyService:
	currency_repository: CurrencyRepository

	def __post_init__(self):
		self.usecase = CurrencyUseCaseFactory(self.currency_repository)

	async def get_currency_list(self):
		return await self.usecase.get_currency_list()

	async def get_currency_by_id(self, id_currency: int):
		return await self.usecase.get_currency_by_id(id_currency)

	async def create_currency(self, command: CreateCurrencyCommand):
		return self.usecase.create_currency(command)

	async def create_currency_and_save(self, command: CreateCurrencyCommand):
		new_currency = self.usecase.create_currency(command)
		currency_from_db = await self.usecase.get_currency_by_code(new_currency.code)
		if currency_from_db:
			raise CurrencyDuplicationException
		return await self.usecase.save_currency(new_currency)

	async def update_currency(self, command: UpdateCurrencyCommand):
		currency = await self.usecase.get_currency_by_id(command.id)
		if not currency:
			raise CurrencyNotFoundException
		currency.sqlmodel_update(command)
		return await self.usecase.save_currency(currency)

	async def save_currency(self, currency: Currency):
		return await self.usecase.save_currency(currency)

	async def delete_currency(self, id_currency: int):
		currency = await self.usecase.get_currency_by_id(id_currency)
		if not currency:
			raise CurrencyNotFoundException
		return await self.usecase.delete_currency(currency)
