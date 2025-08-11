

from dataclasses import dataclass

from core.db import Transactional
from modules.finance.domain.command.currency import CreateCurrencyCommand
from modules.finance.domain.entity.currency import Currency
from modules.finance.domain.repository.currency import CurrencyRepository


@dataclass
class GetCurrencyListUseCase:
	currency_repository : CurrencyRepository

	async def __call__(self):
		return await self.currency_repository.get_currency_list()

@dataclass
class GetCurrencyByIdUseCase:
	currency_repository : CurrencyRepository

	async def __call__(self, id_currency: int):
		return await self.currency_repository.get_currency_by_id(id_currency)

@dataclass
class CreateCurrencyUseCase:

	def __call__(self, command: CreateCurrencyCommand):
		return Currency.model_validate(command)

@dataclass
class SaveCurrencyUseCase:
	currency_repository : CurrencyRepository

	Transactional()
	async def __call__(self, currency: Currency):
		return await self.currency_repository.save(currency)
	
@dataclass
class DeleteCurrencyUseCase:
	currency_repository : CurrencyRepository

	Transactional()
	async def __call__(self, currency: Currency):
		return await self.currency_repository.delete(currency)
	

@dataclass
class CurrencyUseCaseFactory:
	currency_repository: CurrencyRepository

	def __post_init__(self):
		self.get_currency_list = GetCurrencyListUseCase(self.currency_repository)
		self.get_currency_by_id = GetCurrencyByIdUseCase(self.currency_repository)
		self.create_currency = CreateCurrencyUseCase()
		self.save_currency = SaveCurrencyUseCase(self.currency_repository)
		self.delete_currency = DeleteCurrencyUseCase(self.currency_repository)