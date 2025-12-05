import re
from typing import Type, TypeVar, List, Sequence, Set
from datetime import datetime
from sqlmodel import select, and_, col, func
from sqlalchemy import cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from core.search.filters import FilterCriteria, FilterOperator

T = TypeVar("T")


class DynamicSearchMixin:
	"""
	Mixin para repositorios SQLAlchemy que proporciona capacidades de búsqueda dinámica.

	Uso:
		class MyRepository(DynamicSearchMixin):
			model_class = MyModel
			date_fields = {"created_at", "updated_at"}
	"""

	# Clase del modelo - debe ser sobrescrita por la subclase
	model_class: Type[T] = None

	# Campos de fecha del modelo - puede ser sobrescrito por la subclase
	date_fields: Set[str] = set()

	def _build_filter_condition(
		self, filter_criteria: FilterCriteria, model_class: Type[T] = None
	):
		"""
		Construye una condición de filtro basada en el criterio

		Args:
			filter_criteria: Criterio de filtrado
			model_class: Clase del modelo (opcional, usa self.model_class por defecto)

		Returns:
			Condición SQLAlchemy para usar en WHERE

		Raises:
			ValueError: Si el campo no existe, el operador no es válido, o falta un valor requerido
		"""
		target_model = model_class or self.model_class

		if target_model is None:
			raise ValueError(
				"model_class debe ser definido en la clase o pasado como parámetro"
			)

		field_attr = getattr(target_model, filter_criteria.field, None)

		if field_attr is None:
			raise ValueError(
				f"Campo '{filter_criteria.field}' no existe en {target_model.__name__}"
			)

		operator = filter_criteria.operator
		value = filter_criteria.value
		value2 = filter_criteria.value2

		# Convertir valores a date si el campo es de tipo fecha
		if filter_criteria.field in self.date_fields:
			value = self._parse_date_value(value, filter_criteria.field)
			if value2 is not None:
				value2 = self._parse_date_value(value2, filter_criteria.field)

		expr = field_attr
		is_string_col = hasattr(field_attr, "type") and isinstance(
			field_attr.type, String
		)

		if not is_string_col and operator in [
			FilterOperator.CONTAINS,
			FilterOperator.NOT_CONTAINS,
		]:
			expr = cast(field_attr, String)

		# Construir condición según el operador
		if operator == FilterOperator.EQUALS:
			return field_attr == value
		elif operator == FilterOperator.NOT_EQUALS:
			return field_attr != value
		elif operator == FilterOperator.GREATER_THAN:
			return field_attr > value
		elif operator == FilterOperator.GREATER_THAN_OR_EQUAL:
			return field_attr >= value
		elif operator == FilterOperator.LESS_THAN:
			return field_attr < value
		elif operator == FilterOperator.LESS_THAN_OR_EQUAL:
			return field_attr <= value
		elif operator == FilterOperator.CONTAINS:
			return expr.ilike(f"%{value}%")
		elif operator == FilterOperator.NOT_CONTAINS:
			return ~expr.ilike(f"%{value}%")
		elif operator == FilterOperator.BETWEEN:
			if value2 is None:
				raise ValueError("Operador 'between' requiere value2")
			return field_attr.between(value, value2)
		elif operator == FilterOperator.IN:
			if not isinstance(value, list):
				raise ValueError("Operador 'in' requiere una lista de valores")
			return col(field_attr).in_(value)
		elif operator == FilterOperator.NOT_IN:
			if not isinstance(value, list):
				raise ValueError("Operador 'not_in' requiere una lista de valores")
			return col(field_attr).not_in(value)
		elif operator == FilterOperator.IS_NULL:
			return field_attr.is_(None)
		elif operator == FilterOperator.IS_NOT_NULL:
			return field_attr.is_not(None)
		elif operator == FilterOperator.SMART_SEARCH:
			# Supongamos que creas un nuevo Enum FilterOperator.SMART_SEARCH
			# Esto implementa la lógica de dividir palabras que vimos antes
			if not value:
				return True  # O una condición vacía

			terms = list(filter(None, re.split(r"[\s\W]+", str(value))))
			conditions = []
			for word in terms:
				# unaccent(columna) ILIKE unaccent('%palabra%')
				# Esto ignora acentos y mayúsculas
				pattern = f"%{word}%"
				conditions.append(func.unaccent(expr).ilike(func.unaccent(pattern)))

			# Deben cumplirse TODAS las palabras (AND) en ese campo
			return and_(*conditions)
		else:
			raise ValueError(f"Operador '{operator}' no soportado")

	def _parse_date_value(self, value: any, field_name: str):
		"""
		Parsea un valor a date si es un string

		Args:
			value: Valor a parsear
			field_name: Nombre del campo (para mensajes de error)

		Returns:
			date object o None

		Raises:
			ValueError: Si el formato de fecha es inválido
		"""
		if value is not None and isinstance(value, str):
			try:
				return datetime.strptime(value, "%Y-%m-%d").date()
			except ValueError:
				raise ValueError(
					f"El valor '{value}' no es una fecha válida para el campo "
					f"'{field_name}' (formato esperado: YYYY-MM-DD)"
				)
		return value

	async def dynamic_search(
		self,
		session: AsyncSession,
		filters: List[FilterCriteria],
		limit: int = 20,
		page: int = 0,
		model_class: Type[T] = None,
	) -> tuple[List[T] | Sequence[T], int]:
		"""
		Búsqueda dinámica con filtros y paginación

		Args:
			session: Sesión de SQLAlchemy
			filters: Lista de criterios de filtrado
			limit: Límite de resultados por página
			page: Número de página (0-indexed)
			model_class: Clase del modelo (opcional, usa self.model_class por defecto)

		Returns:
			Tupla con (lista de items, total de resultados)

		Raises:
			ValueError: Si algún filtro es inválido
		"""
		target_model = model_class or self.model_class

		if target_model is None:
			raise ValueError(
				"model_class debe ser definido en la clase o pasado como parámetro"
			)

		# Construir condiciones de filtro
		conditions = []
		if filters:
			for filter_criteria in filters:
				condition = self._build_filter_condition(
					filter_criteria, model_class=target_model
				)
				conditions.append(condition)

		# Query para contar total de resultados
		count_query = select(func.count()).select_from(target_model)
		if conditions:
			count_query = count_query.where(and_(*conditions))

		count_result = await session.execute(count_query)
		total = count_result.scalar() or 0

		# Query para obtener los resultados con paginación
		query = select(target_model)
		if conditions:
			query = query.where(and_(*conditions))

		# Aplicar paginación
		offset = page * limit
		query = query.offset(offset).limit(limit)

		result = await session.execute(query)
		items = result.scalars().all()

		return items, total
