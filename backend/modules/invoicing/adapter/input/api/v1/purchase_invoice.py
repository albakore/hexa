import json
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Query, Response

from modules.invoicing.adapter.input.api.v1.request import (
	CreatePurchaseInvoiceRequest,
	SearchPurchaseInvoiceRequest,
)
from modules.invoicing.adapter.input.api.v1.response import PaginatedResponse
from modules.invoicing.container import InvoicingContainer
from modules.invoicing.domain.entity.purchase_invoice import PurchaseInvoice
from shared.interfaces.service_locator import service_locator

# from modules.invoicing.adapter.input.api.v1.request import (
# 	ProviderCreateRequest,
# 	ProviderUpdateRequest,
# )
from modules.invoicing.application.service.purchase_invoice import (
	PurchaseInvoiceService,
)


purchase_invoice_router = APIRouter()


@purchase_invoice_router.get("")
@inject
async def get_all_purchase_invoices(
	limit: int = Query(default=50, ge=1, le=100),
	page: int = Query(default=0),
	service: PurchaseInvoiceService = Depends(
		Provide[InvoicingContainer.purchase_invoice_service]
	),
):
	return await service.get_list(limit, page)


@purchase_invoice_router.get("/of_provider/{id_provider}")
@inject
async def get_all_purchase_invoices_of_provider(
	id_provider: int,
	limit: int = Query(default=50, ge=1, le=100),
	page: int = Query(default=0),
	service: PurchaseInvoiceService = Depends(
		Provide[InvoicingContainer.purchase_invoice_service]
	),
):
	return await service.get_list_of_provider(id_provider, limit, page)


@purchase_invoice_router.get("/search")
@inject
async def search_purchase_invoices(
	q: Optional[str] = Query(
		default=None,
		description='JSON serializado del objeto de búsqueda. Ejemplo: {"filters":[{"field":"invoice_status","operator":"eq","value":"SENDING"}],"limit":20,"page":0}',
	),
	limit: int = Query(default=20, ge=1, le=100),
	page: int = Query(default=0, ge=0),
	service: PurchaseInvoiceService = Depends(
		Provide[InvoicingContainer.purchase_invoice_service]
	),
):
	"""
	Búsqueda dinámica de purchase invoices con filtros personalizables.

	Permite filtrar por cualquier campo de la entidad PurchaseInvoice
	usando diferentes operadores de comparación.

	Respuesta:
	```json
	{
		"items": [...],          // Lista de purchase invoices encontrados
		"total": 150,            // Total de elementos encontrados
		"pages": 8,              // Total de páginas disponibles
		"current_page": 0,       // Página actual
		"limit": 20              // Límite de elementos por página
	}
	```

	Formas de uso:

	1. GET con query parameter 'q' (filtros complejos):
	```
	GET /purchase-invoice/search?q={"filters":[{"field":"invoice_status","operator":"eq","value":"SENDING"},{"field":"fk_provider","operator":"eq","value":1}],"limit":20,"page":0}
	```

	2. GET sin filtros (solo paginación):
	```
	GET /purchase-invoice/search?limit=20&page=0
	```

	3. GET con filtros simples:
	```
	GET /purchase-invoice/search?q={"filters":[{"field":"invoice_status","operator":"eq","value":"SENDING"}]}&limit=20&page=0
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
			command = SearchPurchaseInvoiceRequest.model_validate(search_data)
		except json.JSONDecodeError as e:
			raise ValueError(f"Query parameter 'q' contiene JSON inválido: {str(e)}")
		except Exception as e:
			raise ValueError(f"Error al parsear query parameter 'q': {str(e)}")
	else:
		# Sin filtros, solo usar paginación de query params
		command = SearchPurchaseInvoiceRequest(filters=[], limit=limit, page=page)

	items, total = await service.search_purchase_invoices(command)

	return PaginatedResponse[PurchaseInvoice].create(
		items=list(items), total=total, page=command.page, limit=command.limit
	)


@purchase_invoice_router.get("/{id_purchase_invoice}")
@inject
async def get_purchase_invoices_by_id(
	id_purchase_invoice: int,
	service: PurchaseInvoiceService = Depends(
		Provide[InvoicingContainer.purchase_invoice_service]
	),
):
	return await service.get_one_by_id(id_purchase_invoice)


@purchase_invoice_router.post("")
@inject
async def create_purchase_invoice(
	purchase_invoice: CreatePurchaseInvoiceRequest,
	emit_to_yiqi: bool,
	service: PurchaseInvoiceService = Depends(
		Provide[InvoicingContainer.purchase_invoice_service]
	),
):
	invoice = await service.create(purchase_invoice)
	invoice_saved = await service.save(invoice)

	# Ejecutar task de Celery de forma asíncrona si se solicita
	if emit_to_yiqi:
		yiqi_tasks = service_locator.get_service("yiqi_erp_tasks")
		yiqi_tasks["emit_invoice"].delay(invoice_saved.model_dump())

	return invoice_saved


@purchase_invoice_router.post("/reemit/{id_purchase_invoice}")
@inject
async def reemit_purchase_invoice(
	id_purchase_invoice: int,
	service: PurchaseInvoiceService = Depends(
		Provide[InvoicingContainer.purchase_invoice_service]
	),
):
	return await service.reemit(id_purchase_invoice)
