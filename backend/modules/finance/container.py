from dependency_injector.providers import Factory, Singleton
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from .adapter.output.persistence.currency_adapter import CurrencyRepositoryAdapter
from .adapter.output.persistence.sqlalchemy.currency import CurrencySQLAlchemyRepository
from .application.service.currency import CurrencyService


class FinanceContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(packages=["."], auto_wire=True)

	currency_repository = Singleton(CurrencySQLAlchemyRepository)

	currency_repo_adapter = Factory(
		CurrencyRepositoryAdapter, currency_repository=currency_repository
	)

	currency_service = Factory(
		CurrencyService, currency_repository=currency_repo_adapter
	)
