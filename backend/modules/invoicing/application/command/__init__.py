from datetime import date
import uuid
from enum import Enum
from typing import Any, List
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


###
### DYNAMIC SEARCH
###
class FilterOperator(str, Enum):
	EQUALS = "eq"  # igual a
	NOT_EQUALS = "ne"  # no es / distinto de
	GREATER_THAN = "gt"  # mayor que
	GREATER_THAN_OR_EQUAL = "gte"  # mayor o igual que
	LESS_THAN = "lt"  # menor que
	LESS_THAN_OR_EQUAL = "lte"  # menor o igual que
	CONTAINS = "contains"  # contiene
	NOT_CONTAINS = "not_contains"  # no contiene
	BETWEEN = "between"  # entre (requiere 2 valores)
	IN = "in"  # está en (lista de valores)
	NOT_IN = "not_in"  # no está en (lista de valores)
	IS_NULL = "is_null"  # es nulo
	IS_NOT_NULL = "is_not_null"  # no es nulo


class FilterCriteria(BaseModel):
	field: str = Field(..., description="Campo a filtrar")
	operator: FilterOperator = Field(..., description="Operador de comparación")
	value: Any | None = Field(default=None, description="Valor a comparar")
	value2: Any | None = Field(
		default=None, description="Segundo valor (para operador 'between')"
	)


class SearchPurchaseInvoiceCommand(BaseModel):
	filters: List[FilterCriteria] = Field(
		default=[], description="Lista de filtros a aplicar"
	)
	limit: int = Field(default=20, ge=1, le=50000, description="Límite de resultados")
	page: int = Field(default=0, ge=0, description="Página de resultados")
