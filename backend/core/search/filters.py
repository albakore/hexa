from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class FilterOperator(str, Enum):
	"""Operadores de comparación para filtros dinámicos"""

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
	SMART_SEARCH = "smart_search"  # busqueda inteligente


class FilterCriteria(BaseModel):
	"""Criterio de filtrado para búsqueda dinámica"""

	field: str = Field(..., description="Campo a filtrar")
	operator: FilterOperator = Field(..., description="Operador de comparación")
	value: Any | None = Field(default=None, description="Valor a comparar")
	value2: Any | None = Field(
		default=None, description="Segundo valor (para operador 'between')"
	)
