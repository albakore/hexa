import json
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from modules.provider.adapter.input.api.v1.request import (
	ProviderCreateRequest,
	ProviderUpdateRequest,
	ProviderSearchRequest,
)
from modules.provider.adapter.input.api.v1.response import PaginatedResponse
from modules.provider.application.service.provider import ProviderService
from modules.provider.container import ProviderContainer
from modules.provider.domain.entity.provider import Provider

provider_router = APIRouter()


@provider_router.get("")
@inject
async def get_all_providers(
	limit: int = Query(default=3000, ge=1, le=5000),
	page: int = Query(default=0),
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	return await service.get_all_providers(limit, page)


@provider_router.get("/search")
@inject
async def search_providers(
	q: Optional[str] = Query(
		default=None,
		description='JSON serializado del objeto de búsqueda. Ejemplo: {"filters":[{"field":"name","operator":"contains","value":"ABC"}],"limit":20,"page":0}',
	),
	limit: int = Query(default=20, ge=1, le=100),
	page: int = Query(default=0, ge=0),
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	"""
	Búsqueda dinámica de proveedores con filtros personalizables.

	Permite filtrar por cualquier campo de la entidad Provider
	usando diferentes operadores de comparación.

	Respuesta:
	```json
	{
		"items": [...],          // Lista de proveedores encontrados
		"total": 150,            // Total de elementos encontrados
		"pages": 8,              // Total de páginas disponibles
		"current_page": 0,       // Página actual
		"limit": 20              // Límite de elementos por página
	}
	```

	Formas de uso:

	1. GET con query parameter 'q' (filtros complejos):
	```
	GET /provider/search?q={"filters":[{"field":"name","operator":"contains","value":"ABC"}],"limit":20,"page":0}
	```

	2. GET sin filtros (solo paginación):
	```
	GET /provider/search?limit=20&page=0
	```

	3. GET con filtros por ID:
	```
	GET /provider/search?q={"filters":[{"field":"id","operator":"eq","value":1}]}&limit=20&page=0
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
			command = ProviderSearchRequest.model_validate(search_data)
		except json.JSONDecodeError as e:
			raise ValueError(f"Query parameter 'q' contiene JSON inválido: {str(e)}")
		except Exception as e:
			raise ValueError(f"Error al parsear query parameter 'q': {str(e)}")
	else:
		# Sin filtros, solo usar paginación de query params
		command = ProviderSearchRequest(filters=[], limit=limit, page=page)

	items, total = await service.search_providers(command)

	return PaginatedResponse[Provider].create(
		items=list(items), total=total, page=command.page, limit=command.limit
	)


@provider_router.get("/{id_provider}")
@inject
async def get_provider_by_id(
	id_provider: int,
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	return await service.get_provider_by_id(id_provider)


@provider_router.post("")
@inject
async def create_provider(
	command: ProviderCreateRequest,
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	provider = await service.create_provider(command)
	return await service.save_provider(provider)


@provider_router.put("")
@inject
async def update_provider(
	command: ProviderUpdateRequest,
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	return await service.update_provider(command)


@provider_router.delete("/{id_provider}")
@inject
async def delete_provider(
	id_provider: int,
	service: ProviderService = Depends(Provide[ProviderContainer.provider_service]),
):
	return await service.delete_provider(id_provider)
