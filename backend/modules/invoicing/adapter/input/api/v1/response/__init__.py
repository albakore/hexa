from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
import math

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
	"""Respuesta paginada generica"""

	items: List[T] = Field(..., description="Lista de elementos")
	total: int = Field(..., description="Total de elementos encontrados")
	pages: int = Field(..., description="Total de paginas disponibles")
	current_page: int = Field(..., description="Pagina actual")
	limit: int = Field(..., description="Limite de elementos por pagina")

	@classmethod
	def create(cls, items: List[T], total: int, page: int, limit: int):
		"""Crea una respuesta paginada calculando automaticamente el numero de paginas"""
		pages = math.ceil(total / limit) if limit > 0 else 0
		return cls(
			items=items, total=total, pages=pages, current_page=page, limit=limit
		)
