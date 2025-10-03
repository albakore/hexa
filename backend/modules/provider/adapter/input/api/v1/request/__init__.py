from pydantic import BaseModel
from modules.provider.domain.command import (
	CreateDraftPurchaseInvoiceCommand,
	CreateProviderCommand,
	CreatePurchaseInvoiceServiceCommand,
	UpdateDraftPurchaseInvoiceCommand,
	UpdateProviderCommand,
	UpdatePurchaseInvoiceServiceCommand,
)


class ProviderCreateRequest(CreateProviderCommand): ...


class ProviderUpdateRequest(UpdateProviderCommand): ...


class DraftPurchaseInvoiceCreateRequest(CreateDraftPurchaseInvoiceCommand): ...


class DraftPurchaseInvoiceUpdateRequest(UpdateDraftPurchaseInvoiceCommand): ...


class PurchaseInvoiceServiceCreateRequest(CreatePurchaseInvoiceServiceCommand): ...


class PurchaseInvoiceServiceUpdateRequest(UpdatePurchaseInvoiceServiceCommand): ...
