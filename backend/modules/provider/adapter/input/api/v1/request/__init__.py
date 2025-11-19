from modules.provider.domain.command import (
	CreateDraftPurchaseInvoiceCommand,
	CreateProviderCommand,
	CreatePurchaseInvoiceServiceCommand,
	LinkPurchaseInvoiceServiceToProviderCommand,
	SearchDraftPurchaseInvoiceCommand,
	UpdateDraftPurchaseInvoiceCommand,
	UpdateProviderCommand,
	UpdatePurchaseInvoiceServiceCommand,
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
