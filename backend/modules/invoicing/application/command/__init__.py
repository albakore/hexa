from datetime import date
import uuid
from typing import List
from pydantic import BaseModel, Field

from core.search import FilterOperator, FilterCriteria


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


class SearchPurchaseInvoiceCommand(BaseModel):
	filters: List[FilterCriteria] = Field(
		default=[], description="Lista de filtros a aplicar"
	)
	limit: int = Field(default=20, ge=1, le=50000, description="Límite de resultados")
	page: int = Field(default=0, ge=0, description="Página de resultados")
