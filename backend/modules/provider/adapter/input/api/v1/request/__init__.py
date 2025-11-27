from modules.provider.domain.command import (
	CreateDraftPurchaseInvoiceCommand,
	CreateProviderCommand,
	CreatePurchaseInvoiceServiceCommand,
	LinkPurchaseInvoiceServiceToProviderCommand,
	SearchDraftPurchaseInvoiceCommand,
	SearchProviderCommand,
	SearchPurchaseInvoiceServiceCommand,
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


class LinkPurchaseInvoiceServiceToProviderRequest(
	LinkPurchaseInvoiceServiceToProviderCommand
): ...


class PurchaseInvoiceServiceUpdateRequest(UpdatePurchaseInvoiceServiceCommand): ...


class ProviderSearchRequest(SearchProviderCommand): ...


class PurchaseInvoiceServiceSearchRequest(SearchPurchaseInvoiceServiceCommand): ...


class AirWaybillCreateRequest(CreateAirWaybillCommand): ...


class AirWaybillUpdateRequest(UpdateAirWaybillCommand): ...
