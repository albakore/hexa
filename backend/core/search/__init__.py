"""
Módulo de búsqueda dinámica para repositorios SQLAlchemy

Proporciona clases y mixins reutilizables para implementar búsquedas dinámicas
con filtros en repositorios SQLAlchemy.

Ejemplo de uso:
	from core.search import DynamicSearchMixin, FilterCriteria, FilterOperator

	class MyRepository(DynamicSearchMixin):
		model_class = MyModel
		date_fields = {"created_at", "updated_at"}

		async def search(self, filters, limit, page):
			async with session_factory() as session:
				return await self.dynamic_search(session, filters, limit, page)
"""

from core.search.filters import FilterOperator, FilterCriteria
from core.search.repository import DynamicSearchMixin

__all__ = [
	"FilterOperator",
	"FilterCriteria",
	"DynamicSearchMixin",
]
