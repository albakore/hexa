import uuid
import json
from typing import Optional
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from modules.provider.adapter.input.api.v1.request import (
	DraftPurchaseInvoiceCreateRequest,
	DraftPurchaseInvoiceUpdateRequest,
	DraftPurchaseInvoiceSearchRequest,
)
from modules.provider.adapter.input.api.v1.response import PaginatedResponse
from modules.provider.domain.entity.draft_purchase_invoice import DraftPurchaseInvoice
from modules.provider.application.service.draft_purchase_invoice import (
	DraftPurchaseInvoiceService,
)
from modules.provider.container import ProviderContainer
from modules.provider.domain.command import (
	CreateDraftPurchaseInvoiceCommand,
	UpdateDraftPurchaseInvoiceCommand,
)


draft_invoice_router = APIRouter()


@draft_invoice_router.get("")
@inject
async def get_all_draft_invoices(
	id_provider: int,
	limit: int = Query(default=10, ge=1, le=50),
	page: int = Query(default=0),
	service: DraftPurchaseInvoiceService = Depends(
		Provide[ProviderContainer.draft_invoice_service]
	),
):
	return await service.get_all_draft_purchase_invoices(id_provider, limit, page)


@draft_invoice_router.get("/search")
@inject
async def search_draft_invoices(
	q: Optional[str] = Query(
		default=None,
		description='JSON serializado del objeto de búsqueda. Ejemplo: {"filters":[{"field":"state","operator":"eq","value":"Draft"}],"limit":20,"page":0}',
	),
	limit: int = Query(default=20, ge=1, le=100),
	page: int = Query(default=0, ge=0),
	service: DraftPurchaseInvoiceService = Depends(
		Provide[ProviderContainer.draft_invoice_service]
	),
):
	"""
	Búsqueda dinámica de draft invoices con filtros personalizables.

	Permite filtrar por cualquier campo de la entidad DraftPurchaseInvoice
	usando diferentes operadores de comparación.

	Respuesta:
	```json
	{
		"items": [...],          // Lista de draft invoices encontrados
		"total": 150,            // Total de elementos encontrados
		"pages": 8,              // Total de páginas disponibles
		"current_page": 0,       // Página actual
		"limit": 20              // Límite de elementos por página
	}
	```

	Formas de uso:

	1. GET con query parameter 'q' (filtros complejos):
	```
	GET /draft-invoice/search?q={"filters":[{"field":"state","operator":"eq","value":"Draft"},{"field":"fk_provider","operator":"eq","value":1}],"limit":20,"page":0}
	```

	2. GET sin filtros (solo paginación):
	```
	GET /draft-invoice/search?limit=20&page=0
	```

	3. GET con filtros simples:
	```
	GET /draft-invoice/search?q={"filters":[{"field":"state","operator":"eq","value":"Draft"}]}&limit=20&page=0
	```

	Operadores disponibles:
	- eq: igual a
	- ne: no es / distinto de
	- gt: mayor que
	- gte: mayor o igual que
	- lt: menor que
	- lte: menor o igual que
	- contains: contiene (para strings)
	- not_contains: no contiene
	- between: entre dos valores (requiere value y value2)
	- in: está en lista de valores
	- not_in: no está en lista de valores
	- is_null: es nulo
	- is_not_null: no es nulo
	"""
	# Determinar qué fuente de datos usar
	if q:
		# Parsear el JSON del query parameter
		try:
			search_data = json.loads(q)
			command = DraftPurchaseInvoiceSearchRequest.model_validate(search_data)
			print(command.limit)
		except json.JSONDecodeError as e:
			raise ValueError(f"Query parameter 'q' contiene JSON inválido: {str(e)}")
		except Exception as e:
			raise ValueError(f"Error al parsear query parameter 'q': {str(e)}")
	else:
		# Sin filtros, solo usar paginación de query params
		command = DraftPurchaseInvoiceSearchRequest(filters=[], limit=limit, page=page)

	items, total = await service.search_draft_purchase_invoices(command)

	return PaginatedResponse[DraftPurchaseInvoice].create(
		items=list(items), total=total, page=command.page, limit=command.limit
	)


@draft_invoice_router.get("/{id_draft_invoice}")
@inject
async def get_draft_invoice_by_id(
	id_draft_invoice: int,
	service: DraftPurchaseInvoiceService = Depends(
		Provide[ProviderContainer.draft_invoice_service]
	),
):
	invoice = await service.get_draft_purchase_invoice_by_id(id_draft_invoice)
	invoice_with_metadata = await service.get_draft_purchase_invoice_with_filemetadata(
		invoice
	)
	return invoice_with_metadata


@draft_invoice_router.post("")
@inject
async def create_draft_invoice(
	command: DraftPurchaseInvoiceCreateRequest,
	service: DraftPurchaseInvoiceService = Depends(
		Provide[ProviderContainer.draft_invoice_service]
	),
):
	draft_invoice = await service.create_draft_purchase_invoice(command)
	return await service.save_draft_purchase_invoice(draft_invoice)


@draft_invoice_router.put("/{id_draft_invoice}")
@inject
async def update_draft_invoice(
	id_draft_invoice: int,
	command: DraftPurchaseInvoiceUpdateRequest,
	service: DraftPurchaseInvoiceService = Depends(
		Provide[ProviderContainer.draft_invoice_service]
	),
):
	draft_invoice = UpdateDraftPurchaseInvoiceCommand.model_validate(
		command.model_dump(exclude_unset=True)
	)
	draft_invoice_db = await service.get_draft_purchase_invoice_by_id(id_draft_invoice)
	draft_invoice_db.sqlmodel_update(draft_invoice)
	return await service.save_draft_purchase_invoice(draft_invoice_db)


@draft_invoice_router.delete("/{id_draft_invoice}")
@inject
async def delete_draft_invoice(
	id_draft_invoice: int,
	service: DraftPurchaseInvoiceService = Depends(
		Provide[ProviderContainer.draft_invoice_service]
	),
):
	return await service.delete_draft_purchase_invoice(id_draft_invoice)


@draft_invoice_router.post("/{id_draft_invoice}/emit")
@inject
async def finalize_and_emit_invoice(
	id_draft_invoice: int,
	service: DraftPurchaseInvoiceService = Depends(
		Provide[ProviderContainer.draft_invoice_service]
	),
):
	return await service.finalize_draft(id_draft_invoice)
