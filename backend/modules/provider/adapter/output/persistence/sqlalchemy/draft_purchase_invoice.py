from typing import List, Sequence
from datetime import date, datetime
from sqlmodel import select, and_, or_, col, func
from sqlalchemy import cast, String

from core.db import session_factory, session as global_session
from modules.provider.domain.entity.draft_purchase_invoice import DraftPurchaseInvoice
from modules.provider.domain.repository.draft_purchase_invoice import (
	DraftPurchaseInvoiceRepository,
)
from modules.provider.domain.command import (
	SearchDraftPurchaseInvoiceCommand,
	FilterOperator,
	FilterCriteria,
)


class DraftPurchaseInvoiceSQLAlchemyRepository(DraftPurchaseInvoiceRepository):
	async def get_provider_draft_invoices_list(
		self, id_provider: int, limit: int = 12, page: int = 0
	) -> list[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice]:
		query = select(DraftPurchaseInvoice).where(
			DraftPurchaseInvoice.fk_provider == int(id_provider)
		)
		offset = page * limit
		query = query.offset(offset).limit(limit)

		async with session_factory() as session:
			result = await session.execute(query)

		return result.scalars().all()

	async def get_provider_draft_invoices_by_id(
		self, id_draft_purchase_invoice: int
	) -> DraftPurchaseInvoice | None:
		stmt = select(DraftPurchaseInvoice).where(
			DraftPurchaseInvoice.id == int(id_draft_purchase_invoice)
		)

		async with session_factory() as session:
			instance = await session.execute(stmt)
		return instance.scalars().one_or_none()

	async def save_draft_invoice(
		self, draft_purchase_invoice: DraftPurchaseInvoice
	) -> DraftPurchaseInvoice:
		global_session.add(draft_purchase_invoice)
		await global_session.flush()
		return draft_purchase_invoice

	async def delete_draft_invoice(self, draft_purchase_invoice: DraftPurchaseInvoice):
		await global_session.delete(draft_purchase_invoice)
		await global_session.flush()

	def _build_filter_condition(self, filter_criteria: FilterCriteria):
		"""Construye una condición de filtro basada en el criterio"""
		field_attr = getattr(DraftPurchaseInvoice, filter_criteria.field, None)

		if field_attr is None:
			raise ValueError(f"Campo '{filter_criteria.field}' no existe en DraftPurchaseInvoice")

		operator = filter_criteria.operator
		value = filter_criteria.value
		value2 = filter_criteria.value2

		# Lista de campos de fecha en el modelo
		date_fields = {'service_month', 'issue_date', 'receipt_date'}

		# Convertir valores a date si el campo es de tipo fecha
		if filter_criteria.field in date_fields:
			if value is not None and isinstance(value, str):
				try:
					value = datetime.strptime(value, '%Y-%m-%d').date()
				except ValueError:
					raise ValueError(f"El valor '{value}' no es una fecha válida (formato esperado: YYYY-MM-DD)")

			if value2 is not None and isinstance(value2, str):
				try:
					value2 = datetime.strptime(value2, '%Y-%m-%d').date()
				except ValueError:
					raise ValueError(f"El valor '{value2}' no es una fecha válida (formato esperado: YYYY-MM-DD)")

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
			return cast(field_attr, String).contains(str(value))
		elif operator == FilterOperator.NOT_CONTAINS:
			return ~cast(field_attr, String).contains(str(value))
		elif operator == FilterOperator.BETWEEN:
			if value2 is None:
				raise ValueError(f"Operador 'between' requiere value2")
			return field_attr.between(value, value2)
		elif operator == FilterOperator.IN:
			if not isinstance(value, list):
				raise ValueError(f"Operador 'in' requiere una lista de valores")
			return col(field_attr).in_(value)
		elif operator == FilterOperator.NOT_IN:
			if not isinstance(value, list):
				raise ValueError(f"Operador 'not_in' requiere una lista de valores")
			return col(field_attr).not_in(value)
		elif operator == FilterOperator.IS_NULL:
			return field_attr.is_(None)
		elif operator == FilterOperator.IS_NOT_NULL:
			return field_attr.is_not(None)
		else:
			raise ValueError(f"Operador '{operator}' no soportado")

	async def search_draft_invoices(
		self, command: SearchDraftPurchaseInvoiceCommand
	) -> tuple[List[DraftPurchaseInvoice] | Sequence[DraftPurchaseInvoice], int]:
		"""Búsqueda dinámica de draft invoices con filtros"""
		# Construir condiciones de filtro
		conditions = []
		if command.filters:
			for filter_criteria in command.filters:
				try:
					condition = self._build_filter_condition(filter_criteria)
					conditions.append(condition)
				except ValueError as e:
					# Lanzar excepción si el filtro es inválido
					raise e

		async with session_factory() as session:
			# Query para contar total de resultados
			count_query = select(func.count(DraftPurchaseInvoice.id))
			if conditions:
				count_query = count_query.where(and_(*conditions))

			count_result = await session.execute(count_query)
			total = count_result.scalar() or 0

			# Query para obtener los resultados con paginación
			query = select(DraftPurchaseInvoice)
			if conditions:
				query = query.where(and_(*conditions))

			# Aplicar paginación
			offset = command.page * command.limit
			query = query.offset(offset).limit(command.limit)

			result = await session.execute(query)
			items = result.scalars().all()

		return items, total
