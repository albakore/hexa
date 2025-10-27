from pydantic import BaseModel

from modules.invoicing.application.command import CreatePurchaseInvoiceCommand


class CreatePurchaseInvoiceRequest(CreatePurchaseInvoiceCommand): ...
