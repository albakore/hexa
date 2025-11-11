from pydantic import BaseModel
from modules.finance.domain.command.currency import (
	CreateCurrencyCommand,
	UpdateCurrencyCommand,
)


class CurrencyCreateRequest(CreateCurrencyCommand): ...


class CurrencyUpdateRequest(UpdateCurrencyCommand): ...
