from pydantic import BaseModel
from modules.provider.domain.command import (
	CreateDraftPurchaseInvoiceCommand,
	CreateProviderCommand,
	CreatePurchaseInvoiceServiceCommand,
	UpdateAirWaybillCommand,
	UpdateDraftPurchaseInvoiceCommand,
	UpdateProviderCommand,
	UpdatePurchaseInvoiceServiceCommand,
	SearchDraftPurchaseInvoiceCommand,
	CreateAirWaybillCommand,
)


class ProviderCreateRequest(CreateProviderCommand): ...


class ProviderUpdateRequest(UpdateProviderCommand): ...


class DraftPurchaseInvoiceCreateRequest(CreateDraftPurchaseInvoiceCommand): ...


class DraftPurchaseInvoiceUpdateRequest(UpdateDraftPurchaseInvoiceCommand): ...


class DraftPurchaseInvoiceSearchRequest(SearchDraftPurchaseInvoiceCommand): ...


class PurchaseInvoiceServiceCreateRequest(CreatePurchaseInvoiceServiceCommand): ...


class PurchaseInvoiceServiceUpdateRequest(UpdatePurchaseInvoiceServiceCommand): ...


class AirWaybillCreateRequest(CreateAirWaybillCommand): ...


class AirWaybillUpdateRequest(UpdateAirWaybillCommand): ...
