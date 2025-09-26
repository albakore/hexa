from dependency_injector.providers import Configuration, Container, Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from core.config.settings import env
from modules.finance.adapter.output.persistence.currency_adapter import (
	CurrencyRepositoryAdapter,
)
from modules.finance.adapter.output.persistence.sqlalchemy.currency import (
	CurrencySQLAlchemyRepository,
)
from modules.finance.application.service.currency import CurrencyService


class FinanceContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["modules.finance"], auto_wire=True)

	currency_repository = Singleton(CurrencySQLAlchemyRepository)

	currency_repo_adapter = Factory(
		CurrencyRepositoryAdapter, currency_repository=currency_repository
	)

	currency_service = Factory(
		CurrencyService, currency_repository=currency_repo_adapter
	)
