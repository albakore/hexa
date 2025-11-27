import json
from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from modules.provider.adapter.input.api.v1.request import (
	LinkPurchaseInvoiceServiceToProviderRequest,
	PurchaseInvoiceServiceCreateRequest,
	PurchaseInvoiceServiceUpdateRequest,
	PurchaseInvoiceServiceSearchRequest,
)
from modules.provider.adapter.input.api.v1.response import PaginatedResponse
from modules.provider.application.service.purchase_invoice_service import (
	PurchaseInvoiceServiceTypeService,
)
from modules.provider.container import ProviderContainer
from modules.provider.domain.entity.purchase_invoice_service import (
	PurchaseInvoiceService,
)

purchase_invoice_service_router = APIRouter()


@purchase_invoice_service_router.get("")
@inject
async def get_all_services(
	limit: int = Query(default=3000, ge=1, le=5000),
	page: int = Query(default=0),
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	return await service.get_all_services(limit, page)


@purchase_invoice_service_router.get("/search")
@inject
async def search_services(
	q: Optional[str] = Query(
		default=None,
		description='JSON serializado del objeto de búsqueda. Ejemplo: {"filters":[{"field":"name","operator":"contains","value":"logistics"}],"limit":20,"page":0}',
	),
	limit: int = Query(default=20, ge=1, le=100),
	page: int = Query(default=0, ge=0),
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	"""
	Búsqueda dinámica de servicios de factura con filtros personalizables.

	Permite filtrar por cualquier campo de la entidad PurchaseInvoiceService
	usando diferentes operadores de comparación.

	Respuesta:
	```json
	{
		"items": [...],          // Lista de servicios encontrados
		"total": 150,            // Total de elementos encontrados
		"pages": 8,              // Total de páginas disponibles
		"current_page": 0,       // Página actual
		"limit": 20              // Límite de elementos por página
	}
	```

	Formas de uso:

	1. GET con query parameter 'q' (filtros complejos):
	```
	GET /purchase-invoice-service/search?q={"filters":[{"field":"group","operator":"eq","value":"Logistics"}],"limit":20,"page":0}
	```

	2. GET sin filtros (solo paginación):
	```
	GET /purchase-invoice-service/search?limit=20&page=0
	```

	3. GET con filtros por nombre:
	```
	GET /purchase-invoice-service/search?q={"filters":[{"field":"name","operator":"contains","value":"shipping"}]}&limit=20&page=0
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
			command = PurchaseInvoiceServiceSearchRequest.model_validate(search_data)
		except json.JSONDecodeError as e:
			raise ValueError(f"Query parameter 'q' contiene JSON inválido: {str(e)}")
		except Exception as e:
			raise ValueError(f"Error al parsear query parameter 'q': {str(e)}")
	else:
		# Sin filtros, solo usar paginación de query params
		command = PurchaseInvoiceServiceSearchRequest(filters=[], limit=limit, page=page)

	items, total = await service.search_services(command)

	return PaginatedResponse[PurchaseInvoiceService].create(
		items=list(items), total=total, page=command.page, limit=command.limit
	)


@purchase_invoice_service_router.get("/{id_purchase_invoice_service}")
@inject
async def get_service_by_id(
	id_purchase_invoice_service: int,
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	return await service.get_services_by_id(id_purchase_invoice_service)


@purchase_invoice_service_router.post("")
@inject
async def create_service(
	command: PurchaseInvoiceServiceCreateRequest,
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	new_command = await service.create_purchase_invoice_service(command)
	service = await service.save_purchase_invoice_service(new_command)
	return service


@purchase_invoice_service_router.get("/get-from/provider/{id_provider}")
@inject
async def get_services_of_provider(
	id_provider: int,
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	return await service.get_services_of_provider(id_provider)


@purchase_invoice_service_router.post("/add-to/provider/{id_provider}")
@inject
async def add_services_to_provider(
	id_provider: int,
	services: List[LinkPurchaseInvoiceServiceToProviderRequest],
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	return await service.add_services_to_provider(id_provider, services)


@purchase_invoice_service_router.delete("/remove-from/provider/{id_provider}")
@inject
async def remove_services_from_provider(
	id_provider: int,
	id_services_list: List[int],
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	return await service.remove_services_from_provider(id_provider, id_services_list)


@purchase_invoice_service_router.put("")
@inject
async def update_service(
	command: PurchaseInvoiceServiceUpdateRequest,
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	service_updated = await service.update_purchase_invoice_service(command)
	return service_updated


@purchase_invoice_service_router.delete("/{id_purchase_invoice_service}")
@inject
async def delete_service(
	id_purchase_invoice_service: int,
	service: PurchaseInvoiceServiceTypeService = Depends(
		Provide[ProviderContainer.invoice_servicetype_service]
	),
):
	service_updated = await service.delete_purchase_invoice_service(
		id_purchase_invoice_service
	)
	return service_updated
