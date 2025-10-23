from datetime import date
import uuid
from pydantic import BaseModel, Field


class CreatePurchaseInvoiceCommand(BaseModel):
	fk_provider: int
	fk_service: int
	number: str
	concept: str
	issue_date: date
	receipt_date: date
	service_month: date
	period_from_date: date | None = Field(default=None)
	period_until_date: date | None = Field(default=None)
	currency: str
	unit_price: float
	air_waybill: str | None = Field(default=None)
	kilograms: float | None = Field(default=None)
	items: int | None = Field(default=None)
	fk_receipt_file: uuid.UUID
	fk_detail_file: uuid.UUID | None = Field(default=None)
