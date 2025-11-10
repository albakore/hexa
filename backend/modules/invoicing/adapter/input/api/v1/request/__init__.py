from pydantic import BaseModel

from modules.invoicing.application.command import (
	CreatePurchaseInvoiceCommand,
	SearchPurchaseInvoiceCommand,
)


class CreatePurchaseInvoiceRequest(CreatePurchaseInvoiceCommand): ...


class SearchPurchaseInvoiceRequest(SearchPurchaseInvoiceCommand): ...
