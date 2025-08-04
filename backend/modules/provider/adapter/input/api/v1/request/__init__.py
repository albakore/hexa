from pydantic import BaseModel
from modules.provider.domain.command import (
	CreateDraftPurchaseInvoiceCommand,
	CreateProviderCommand,
	UpdateDraftPurchaseInvoiceCommand,
	UpdateProviderCommand,
)


class ProviderCreateRequest(CreateProviderCommand): ...


class ProviderUpdateRequest(UpdateProviderCommand): ...


class DraftPurchaseInvoiceCreateRequest(CreateDraftPurchaseInvoiceCommand): ...


class DraftPurchaseInvoiceUpdateRequest(UpdateDraftPurchaseInvoiceCommand): ...
